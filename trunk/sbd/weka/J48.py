#/usr/bin/env python
# -*- coding:utf8 -*-
import sys

import java.io.FileReader as FileReader
import java.io.FileInputStream as FileInputStream
import java.io.InputStream as InputStream
import java.io.InputStreamReader as InputStreamReader
import java.io.ObjectInputStream as ObjectInputStream
import java.io.BufferedReader as BufferedReader
import weka.core.Instances as Instances
import weka.classifiers.trees.J48 as J48
import weka.core.Utils as Utils

class DecisionTree:
    def __init__(self, model=None, arff=None):
        try:
            if model != None and arff != None:
                self.j48 = self.load_model(model, arff)
            else:
                self.j48 = J48()
        except:
            raise

    def load_arff(self, arff):
        file = FileReader(arff)

        #fis = FileInputStream(arff)
        #file = InputStreamReader(fis, "UTF-8");

        #fr = FileReader(arff)
        #file = BufferedReader(fr)
        
        data = Instances(file)
        data.setClassIndex(data.numAttributes() - 1)
        return data

    def build_model(self, data):
        self.j48.buildClassifier(data)

    def load_model(self, model, arff):
        try:
            j48 = J48()
            options = ('-i', '-l', model, '-T', arff)
            objectInputFileName = Utils.getOption('l', options);
            if len(objectInputFileName) == 0:
                print "No training file and no object input file given."
                raise
            inputStream = InputStream
            inputStream = FileInputStream(objectInputFileName)
            objectInputStream = ObjectInputStream(inputStream)
            j48 = objectInputStream.readObject()
            return j48
        except:
            raise

    def print_this(self):
        print self.j48

    def print_instance(self, data):
        i = 0
        while True:
            try:
                myinstance = data.instance(i)
                line = str(myinstance)
                ptype, ppos, spos, psyll_1, ssyll_1, psyll_2, ssyll_2, psyll_3, ssyll_3, ptoken, stoken, pdist, sdist, psize, ssize, sbd = line.split(',')
                klass = self.j48.classifyInstance(myinstance)
                result = data.attribute(data.classIndex()).value(int(klass))
                #if test != result:
                i += 1
                print i, sbd, result
            except:
                import traceback
                import sys
                traceback.print_exc(file=sys.stderr)
                break

    def classifyInstance(self, instance):
        pass

def print_usage():
    print 'python J48.py [model-filename] [arff-filename] [test | build]'
    print 'python J48.py j48.model test.arff test'

def exit(err=None):
    sys.exit(err)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage()
        exit()
    MODEL = sys.argv[1]
    ARFF = sys.argv[2]
    FUNC = sys.argv[3]

    dt = DecisionTree(MODEL, ARFF)
    data = dt.load_arff(ARFF)
    if FUNC == 'test':
        dt.print_instance(data)
    else:
        dt.build_model(data)
        dt.print_this()

    exit()

