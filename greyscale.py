import tensorflow as tf
import pandas as pd
import numpy as np
import os
import pathlib
import cv2
import string
from keras import layers, models
import matplotlib.pyplot as plt

image_shape = (256, 256, 3)
kernel = 5
padding = 'same'
learning_rate = 0.0001
weight_decay = 6e-8
filter = 16
strides = 1
source_input = layers.Input(shape = image_shape, name = 'source')
target_input = layers.Input(shape = image_shape, name = 'target')
def inceptionModule(inputs, filter, kernel, padding, strides, activation, use_norm):
    x = inputs
    x = layers.Conv2D(filter, kernel_size = kernel, padding = padding, strides = strides,
                    dilation_rate = 1)(x)
    x = layers.Activation(activation)(x)
    if use_norm:
        x = layers.GroupNormalization(groups = 1)(x)
    x = layers.Conv2D(filter, kernel_size = kernel, padding = padding, strides = strides,
                      dilation_rate = 1)(x)
    x = layers.Activation(activation)(x)
    if use_norm:
        x = layers.GroupNormalization(groups = 1)(x)
    x = layers.Conv2D(filter, kernel_size = kernel, padding = padding, strides = strides,
                      dilation_rate = 1)(x)
    x = layers.Activation(activation)(x)
    if use_norm:
        x = layers.GroupNormalization(groups = 1)(x)
    return x
def convolution(inputs, filters, kernel, padding, strides, activation, use_norm):
    x = inputs
    x = inceptionModule(x, filters, kernel, padding, strides, activation, use_norm)
    y = layers.Conv2D(filters, kernel_size = 1, padding = padding, strides = strides,
                                     activation = activation,)(inputs)
    if use_norm:
      y = layers.GroupNormalization(groups = 1)(y)

    x = layers.add([x, y])
    return x
def encoder(inputs, filters, padding, strides, activation, kernel, use_norm):
    conv = convolution(inputs, filters, kernel, padding, strides, activation, use_norm)
    return layers.Conv2D(filters, kernel_size = 1, padding = padding, strides = 2, activation = activation)(conv), conv
def decoder(inputs, skip, filters, padding, strides, kernel, activation, use_norm):
    x = layers.Conv2DTranspose(filters, kernel_size = kernel, padding = padding,
                              strides = 2, activation = activation,)(inputs)
    x = layers.add([x, skip])
    x = convolution(x, filters, kernel ,padding, strides, activation, use_norm)
    return x

def U_net(inputs, filter, padding, strides, activation, kernel, use_norm, name, weights):
    x = inputs
    conv1, skip1 = encoder(x, filter, padding, strides, activation[0], kernel, use_norm)
    conv2, skip2 = encoder(conv1, filter*2, padding, strides, activation[0], kernel, use_norm)
    conv3, skip3 = encoder(conv2, filter*4, padding, strides, activation[0], kernel, use_norm)
    conv4, skip4 = encoder(conv3, filter*8, padding, strides, activation[0], kernel, use_norm)
    conv5, skip5 = encoder(conv4, filter*16, padding, strides, activation[0], kernel, use_norm)
    x = layers.Flatten()(conv5)
    x = layers.Dense(128, name = 'latent_space',
                     kernel_regularizer = tf.keras.regularizers.L2(0.001))(x)
    x = layers.Dense(conv5.shape[1]*conv5.shape[2]*conv5.shape[3],
                    kernel_regularizer = tf.keras.regularizers.L2(0.001),)(x)
    x = layers.Reshape((conv5.shape[1], conv5.shape[2], conv5.shape[3]))(x)
    dec1 = decoder(x, skip5, filter*16, padding, strides, kernel, activation[1], use_norm)
    dec2 = decoder(dec1, skip4, filter*8, padding, strides, kernel, activation[1], use_norm)
    dec3 = decoder(dec2, skip3, filter*4, padding, strides, kernel, activation[1], use_norm)
    dec4 = decoder(dec3, skip2, filter*2, padding, strides, kernel, activation[1], use_norm)
    dec5 = decoder(dec4, skip1, filter, padding, strides, kernel, activation[1], use_norm)
    dec5 = layers.concatenate([
    dec5,
    layers.GroupNormalization(groups = 1)(layers.Conv2DTranspose(filter, kernel_size = kernel, padding = 'same', strides = 16,
                                                       activation = activation[1])(dec1)),
                              ])
    output = layers.Conv2DTranspose(3, kernel_size = kernel, padding = padding,
                                   strides = 1,)(dec5)
    output = layers.Activation('sigmoid')(output)
    m = models.Model(inputs = inputs, outputs = output,
                    name = name)
    if weights:
      if name == 'xTOy':
          m.load_weights('/kaggle/working/g_target.h5')
      elif name == 'yTOx':
          m.load_weights('/kaggle/working/g_source.h5')
    return m

def Discriminator(inputs, filter, padding, strides, kernel, activation, use_norm,
                 name, weights):
    x = inputs
    conv1, skip1 = encoder(x, filter, padding, strides, activation, kernel, use_norm)
    conv2, skip2 = encoder(conv1, filter*2, padding, strides, activation, kernel, use_norm)
    conv3, skip3 = encoder(conv2, filter*4, padding, strides, activation, kernel, use_norm)
    conv4, skip4 = encoder(conv3, filter*8, padding, strides, activation, kernel, use_norm)
    conv5, skip5 = encoder(conv4, filter*16, padding, strides, activation, kernel, use_norm)
    output = layers.Conv2D(1, kernel_size = kernel, padding = padding,
                         strides = 1)(conv5)
    output1 = layers.Conv2D(1, kernel_size = kernel, padding = padding,
                         strides = 1)(conv4)
    output2 = layers.Conv2D(1, kernel_size = kernel, padding = padding,
                         strides = 1)(conv3)
    m = models.Model(inputs = inputs, outputs = [output, output1, output2,], name = name)
    if weights:
      if name == 'xx':
          m.load_weights('/kaggle/working/d_source.h5')
      elif name == 'yy':
          m.load_weights('/kaggle/working/d_target.h5')
    return m
g_target = U_net(source_input, filter, padding,
                        strides, ['LeakyReLU', 'relu'], kernel, use_norm = True,
                        name = 'xTOy', weights = True)
g_source = U_net(target_input, filter, padding, strides,
                       ['LeakyReLU', 'relu'], kernel, use_norm = True,
                       name = 'yTOx', weights = True)
# discriminator source
d_source = Discriminator(source_input, filter, 'same', 1, kernel, 'LeakyReLU', use_norm = False,
                        name = 'xx', weights = True)
# discriminator target
d_target = Discriminator(target_input, filter, 'same', 1, kernel, 'LeakyReLU', use_norm = False,
                        name = 'yy', weights = True)
d_source.compile(loss = ['mse',  'mse', 'mse'],
                 optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate))
d_target.compile(loss = ['mse',  'mse', 'mse'],
                 optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate))
d_source.trainable = False
d_target.trainable = False
# forward cyclegan
recon_target_forward = g_target(source_input)
d_target_re = d_target(recon_target_forward)
recon_source_forward = g_source(recon_target_forward)
# backward cyclegan
recon_source_backward = g_source(target_input)
d_source_re = d_source(recon_source_backward)
recon_target_backward = g_target(recon_source_backward)
# for identity
iden_target = g_target(target_input)
iden_source = g_source(source_input)
gan = models.Model(inputs = [source_input, target_input],
                  outputs = [d_target_re, d_source_re,
                            recon_source_forward,
                            recon_target_backward,
                            iden_source,
                            iden_target
                             ],
                  name = 'generative_gan')
loss_weights = [1, 1, 1, 1, 1, 1, 10, 10, 0.5, 0.5]
losses = ['mse', 'mse', 'mse', 'mse', 'mse', 'mse', 'mae', 'mae', 'mae', 'mae']
gan.compile(loss = losses, optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate*0.5,),
           loss_weights = loss_weights)
gan.output