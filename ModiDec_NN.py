import tensorflow as tf
from keras.models import Model
from keras.layers import Conv1D, MaxPooling1D , Add, Dropout , Dense , Conv2D
from keras.layers import Input, Activation , Concatenate, LSTM ,  BatchNormalization, Reshape
from keras.layers import Resizing , Masking, Multiply



def Conv1D_swish_bn(x, N_filters, kernel, strides):

    x = Conv1D(N_filters, kernel, strides=strides, padding="same")(x)
    x = BatchNormalization()(x)
    x = Activation("swish")(x)

    return x


def Conv2D_swish_bn(x, N_filters, kernel, strides):

    x = Conv2D(N_filters, kernel, strides=strides, padding="same")(x)
    x = BatchNormalization()(x)
    x = Activation("swish")(x)

    return x


def Inception_res_block(x, N_filters):

    short = Conv1D(N_filters, 1, strides = 1, padding="same")(x)
    short = BatchNormalization()(short)

    x_Inc_1 = Conv1D_swish_bn(x, int(0.2*N_filters), kernel= 1, strides= 1)
    x_Inc_2 = Conv1D_swish_bn(x_Inc_1, int(0.35*N_filters), kernel= 3, strides= 1)
    x_Inc_3 = Conv1D_swish_bn(x_Inc_2, int(0.5*N_filters), kernel= 5, strides= 1)

    x_conc = Concatenate(axis=-1)([x_Inc_1, x_Inc_2, x_Inc_3])
    x_conc = Conv1D(N_filters, 1, strides=1, padding="same")(x_conc)
    x_conc = BatchNormalization()(x_conc)

    out = Add()([short,x_conc])
    out = BatchNormalization()(out)
    out = Activation("swish")(out)

    return out

def Inception_res_block_2D(x, N_filters, kernel):

    short = Conv2D(N_filters, 1, strides = 1, padding="same")(x)
    short = BatchNormalization()(short)

    x_Inc_1 = Conv2D_swish_bn(x, int(0.2*N_filters), kernel= 1, strides= 1)
    x_Inc_2 = Conv2D_swish_bn(x_Inc_1, int(0.35*N_filters), kernel= kernel, strides= 1)
    x_Inc_3 = Conv2D_swish_bn(x_Inc_2, int(0.5*N_filters) + 1, kernel= kernel, strides= 1)

    x_conc = Concatenate(axis=-1)([x_Inc_1, x_Inc_2, x_Inc_3])

    # Final 1x1 Conv to reduce dimensions to N_filters
    x_conc = Conv2D(N_filters, 1, strides=1, padding="same")(x_conc)
    x_conc = BatchNormalization()(x_conc)

    out = Add()([short,x_conc])
    out = BatchNormalization()(out)
    out = Activation("swish")(out)

    return out


def ModiDeC_model(Inp_1, Inp_2, labels, kmer_model):

    input_layer1 = Input((Inp_1,1), name='Input_1')

    x1 = Inception_res_block(input_layer1,256)
    x1 = MaxPooling1D(2)(x1)
    x1 = tf.keras.layers.Bidirectional(LSTM(128, return_sequences=True))(x1)

    x1 = Inception_res_block(x1,512)
    x1 = MaxPooling1D(2)(x1)
    x1 = tf.keras.layers.Bidirectional(LSTM(256, return_sequences=True))(x1)

    x1 = Inception_res_block(x1,1024)
    x1 = MaxPooling1D(2)(x1)
    x1 = tf.keras.layers.Bidirectional(LSTM(512, return_sequences=True))(x1)

    x1 = Reshape((Inp_2, int(x1.shape[1]*1024/Inp_2)))(x1)

    input_layer2 = Input((Inp_2,4,1), name='Input_2')
    masked_input = Masking(mask_value=0.0)(input_layer2)

    x2 = Inception_res_block_2D(masked_input , 128, (kmer_model,4))
    x2 = Inception_res_block_2D(x2 , 256, (3,3))

    x2 = Reshape((x2.shape[-3], x2.shape[-2] * x2.shape[-1]))(x2)
    x2 = Inception_res_block(x2,512) # 512

    x_con = Concatenate(axis=-1)([x1,x2])

    x_con = Dense(1024)(x_con)
    x_con = BatchNormalization()(x_con)
    x_con = Activation("swish")(x_con)

    x_con = Dropout(0.2)(x_con)

    x_con = Dense(1024)(x_con)
    x_con = BatchNormalization()(x_con)
    x_con = Activation("swish")(x_con)

    x_con = Dropout(0.2)(x_con)

    x_LSTM = tf.keras.layers.Bidirectional(LSTM(256, return_sequences=True))(x_con)

    out_2 = Dense(labels, activation="sigmoid")(x_LSTM)
    model = Model(inputs = [input_layer1, input_layer2] , outputs = [out_2])

    return model
 