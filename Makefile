DEBUG=1
STATIC=1
CC=gcc
CXX=g++

#CPPFLAGS+=-fno-gnu-unique
CPPFLAGS+=-Wall -fPIC

LDFLAGS+=-shared

# LDFLAGS+= -pthread -ldl -lrt

# LDFLAGS+=-Wl,-rpath,'$$ORIGIN/'
# LDFLAGS+=-Wl,--dynamic-linker,./ld-2.17.so

ifeq ($(DEBUG), 1)
	CPPFLAGS += -g3 -DDEBUG -std=gnu++0x -D_GLIBCXX_USE_NANOSLEEP -O0 -DTIXML_USE_STL
else
	CPPFLAGS += -g3 -O3 -Os -DNDEBUG -std=gnu++0x -D_GLIBCXX_USE_NANOSLEEP -DTIXML_USE_STL
endif

ifeq ($(STATIC), 1)
	LDFLAGS += -static-libgcc -static-libstdc++
endif

INCPATH += -I./
# INCPATH+=-I../../../../publib/Common/C/tinyxml_2_6_2/
INCPATH+=-I../../../../publib/Common/C/Linux/
INCPATH+=-I../../../../publib/Common/C/
# INCPATH+=-I../../../../publib/3rdParty/C/Linux/libopenssl/include/
CPPFLAGS+=$(INCPATH)

LIBS+=-Wl,--as-needed
# SSL_LIBS+=../../../../publib/3rdParty/C/Linux/libopenssl/lib/libssl.a ../../../../publib/3rdParty/C/Linux/libopenssl/lib/libcrypto.a
# LIBS+=$(SSL_LIBS)
LIBS+=../../../../publib/Common/C/Linux/libjson/lib/libjson.a
LIBS+=../../../../publib/Common/C/Linux/minizip/libminizip.a
LIBS+=../../../../publib/3rdParty/C/Linux/libz/lib/libz.a
LIBS+= -lpthread -ldl -lrt

COMMON_OBJS+=../../../../publib/Common/C/Linux/EcTimer.o
COMMON_OBJS+=../../../../publib/Common/C/Linux/MyLog.o
COMMON_OBJS+=../../../../publib/Common/C/Linux/INIParser.o
COMMON_OBJS+=../../../../publib/Common/C/Linux/CSimpleThread.o
COMMON_OBJS+=../../../../publib/Common/C/Linux/ProcessLock.o
COMMON_OBJS+=../../../../publib/Common/C/Linux/helputility.o
COMMON_OBJS+=../../../../publib/Common/C/Linux/md5.o
COMMON_OBJS+=../../../../publib/Common/C/Linux/wdmd5.o


PROCESS_OBJS+=SystemSecurityPlugin.o SystemSecurityPolicyHandler.o SystemSecurityThread.o SystemSecurityInspect.o BaseInfo.o

OBJS+=$(COMMON_OBJS)
OBJS+=$(PROCESS_OBJS)

PROCESS_LIB=../../framework/SystemSecurity.so

TARGET=$(PROCESS_LIB)

.PHONY:all clean
all: $(TARGET)


ALWAYSMAKE:

$(PROCESS_LIB): $(OBJS)
	$(CXX) $(CPPFLAGS) $(SHAREFLAGS) -o $(PROCESS_LIB) $^ $(LDFLAGS) $(LIBS)

clean:
	rm -rf $(OBJS) $(TARGET) core.*
