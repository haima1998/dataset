mv no_bn.prototxt MobileNetSSD_deploy.prototxt
mv no_bn.caffemodel MobileNetSSD_deploy.caffemodel

~/disk1/code/opensouce/caffe/caffe/build/tools/upgrade_net_proto_text MobileNetSSD_deploy.prototxt MobileNetSSD_deploy_new.prototxt
~/disk1/code/opensouce/caffe/caffe/build/tools/upgrade_net_proto_binary MobileNetSSD_deploy.caffemodel MobileNetSSD_deploy_new.caffemodel

~/disk1/code/opensouce/ncnn/build/tools/caffe/caffe2ncnn MobileNetSSD_deploy_new.prototxt MobileNetSSD_deploy_new.caffemodel MobileNetSSD_deploy.param MobileNetSSD_deploy.bin
~/disk1/code/opensouce/ncnn/build/tools/ncnn2mem MobileNetSSD_deploy.param MobileNetSSD_deploy.bin MobileNetSSD_deploy.id.h MobileNetSSD_deploy.mem.h
