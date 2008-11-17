#!/bin/bash
./build-model.sh weka weka/sejong.arff model/sejong_weka_j48.model weka/sejong_j48.out
./build-model.sh weka weka/pentree.arff model/pentree_weka_j48.model weka/pentree_j48.out
./build-model.sh maxent maxent/sejong.maxent model/sejong_maxent.model maxent/sejong_maxent.out
./build-model.sh maxent maxent/pentree.maxent model/pentree_maxent.model maxent/pentree_maxent.out
