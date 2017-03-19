from PIL import Image, ImageDraw, ImageOps
from fann2 import libfann


desired_error = 0.00001
max_iterations = 100000
iterations_between_reports = 5

traindata = libfann.training_data()
traindata.read_train_from_file("dataset.data")
testdata = libfann.training_data()
testdata.read_train_from_file("testdata.data")


ann = libfann.neural_net()
ann.create_standard_array((900,100,48))
ann.set_learning_rate(0.7)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC_STEPWISE)
ann.set_activation_steepness_hidden(0.4)
ann.set_activation_steepness_output(0.4)
#ann.train_on_file("dataset.data", max_iterations, iterations_between_reports, desired_error)
done = 0
epoch = 1
while done != 1:
    ann.train_epoch(traindata)
    print epoch, ":   Train MSE: ", ann.get_MSE(), ann.get_bit_fail()
    ann.reset_MSE()
    ann.get

    ann.test_data(testdata)
    print "Test MSE: ", ann.get_MSE(), "Test Bit Fail: ", ann.get_bit_fail()
    if ann.get_MSE() < 0.001:
        done = 1
    epoch += 1
ann.reset_MSE()
#ann.test_data(data)

print(str(ann.get_MSE()) + "!!!")

ann.save("network.net")