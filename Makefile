
DEST = ..

KOR_RULE_PATH = $(DEST)/kor-rule-sbd
KOR_ML_PATH = $(DEST)/kor-ml-sbd
ENG_ML_PATH = $(DEST)/eng-ml-sbd

EXCLUDE = '*.pyc'
CP = rsync -a --exclude $(EXCLUDE)

# PYTHON = python2.5
# JAVA = java1.6.0
# JYTHON = jython2.2.1
# WEKA = weka3.5.7
# MYSQL = mysql-connector for weka
# LIBSVM = libsvm for weka
# MAXENT = maxent for python

JAVA = java -Xmx2048m
CLASSPATH = /usr/local/mysql-jdbc/mysql-connector-java-5.0.8-bin.jar:jar/weka.jar:jar/libsvm.jar

CLASSIFIER = weka.classifiers.trees.J48
INSTANCE = instance/pentree.arff 
MODEL = model/j4i.model
CFLAGS = -C 0.25 -M 2 -t $(INSTANCE) -d $(MODEL)

# DIRECTORY
SOURCES = corpus sbd dict

# FILE
PYTYHONS = Tokenizer.py Builder.py Learner.py Evaluator.py
BASHES = build-dict.sh build-instances.sh evaluator.sh
OTHERS = README

 
TARGET = kor-rule
 
# Implict rules 
.SUFFIXES:.py .sh 
 
# build rule 
 
all: $(TARGET) 
 
# copy
kor-rule:
	$(CP) $(SOURCES) $(KOR_RULE_PATH)
	$(CP) $(PYTHONS) $(KOR_RULE_PATH)
	$(CP) $(BASHES) $(KOR_RULE_PATH)
	$(CP) $(OTHERS) $(KOR_RULE_PATH)

