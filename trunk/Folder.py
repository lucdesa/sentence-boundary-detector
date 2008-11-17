#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
import sys

class Util(object):
    def get_total_lineno(filename):
        import os
        import time
        os.system('cat ./' + filename + ' | wc -l > lineno')
        file = open('lineno', 'r')
        lineno = int(file.readline().strip())
        file.close()
        os.system('rm -rf lineno')
        return lineno

    def split_filename(number):
        return str(number) + '.split'

    def learn_filename(number):
        return str(number) + '.learn'

    def eval_filename(number):
        return str(number) + '.evals'

    getTotalLineno = staticmethod(get_total_lineno)
    getSplitFilename = staticmethod(split_filename)
    getLearnFilename = staticmethod(learn_filename)
    getEvalFilename = staticmethod(eval_filename)

class Divider:
    def __init__(self, filename):
        self.file = open(filename)
        self.opened = True

    def __del__(self):
        self.close()

    def close(self):
        if (self.opened):
            self.file.close()

    def fold_sequential(self, out, fold):
        import time
        files = []
        totalcount = 0
        for number in xrange(fold):
            filename = Util.getSplitFilename(number)
            totalcount += Util.getTotalLineno(filename)
            file = open(out + '/' + filename, 'w+')
            files.append(file)

        percount = totalcount / 10
        count = 0
        number = 1
        for line in self.file:
            count += 1
            if count < percount*number:
                dot = ''
                if number > 9:
                    number = 10
                    dot += dot
                files[number-1].write(line)
            else:
                print str(percount*number) + " number"
                number += 1

        print 'dot :' + dot
        for file in files:
            file.close()

    def fold_random(self, out, fold):
        files = []
        for number in xrange(fold):
            filename = Util.getSplitFilename(number)
            file = open(out + '/' + filename, 'w+')
            files.append(file)
        
        for line in self.file:
            import random
            number = random.randint(0, fold-1)
            files[number].write(line)

        for file in files:
            file.close()

class Generator:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def generate(self, out, fold):
        import os
        for i in xrange(fold):
            for j in xrange(fold):
                if i == j:  # evaluation-file
                    splitfilename = Util.getSplitFilename(i)
                    evalfilename = Util.getEvalFilename(j)
                    shell = 'cat ' + out + '/' + splitfilename + ' >> ' + out + '/' + evalfilename
                    os.system(shell)
                else:            # learning-file
                    splitfilename = Util.getSplitFilename(i)
                    learnfilename = Util.getLearnFilename(j)
                    shell = 'cat ' + out + '/' + splitfilename + ' >> ' + out + '/' + learnfilename
                    os.system(shell)

def print_usage():
    print '\tUsage:   python Folder.py filename outputfolder foldnumber [ random | sequential ]'
    print '\tExample: python Folder.py corpus/sample/sample.raw tenfolds/sample 10 random'
    print '\tExample: python Folder.py corpus/sejong/sejong.raw tenfolds/sejong 10 random'
    print '\tExample: python Folder.py corpus/pentree/pentree.raw tenfolds/pentree 10 random'

if __name__ == '__main__':
    try:
        if len(sys.argv) != 5:
            print_usage()
        else:
            # parse argument
            filename = sys.argv[1]
            outfolder = sys.argv[2]
            fold = int(sys.argv[3])
            func = sys.argv[4]

            # Folder 0.split~9.split files
            div = Divider(filename)
            if func == 'random':
                div.fold_random(outfolder, fold)
            elif func == 'sequential':
                div.fold_sequential(outfolder, fold)
            else:
                div.fold_random(outfolder, fold)
            del div
            # genrating 0.learn,0.evals~9.learn,9.evals files
            gen = Generator()
            gen.generate(outfolder,fold)
            del gen
    except:
        traceback.print_exc(file=sys.stderr)
