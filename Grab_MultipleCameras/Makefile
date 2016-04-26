# Makefile for Basler pylon sample program
.PHONY: all clean

# The program to build
NAME1       := Grab_MultipleCameras
NAME2       := AlignImages


# Installation directories for pylon
PYLON_ROOT ?= /opt/pylon5


CPPFLAGS = $(shell pkg-config opencv --cflags --libs)

LDFLAGS = $(shell pkg-config opencv --cflags --libs)


# Build tools and flags
LD         := $(CXX)
CPPFLAGS   := $(shell $(PYLON_ROOT)/bin/pylon-config --cflags) -DUSE_GIGE
CPPFLAGS += `pkg-config --cflags opencv`
CXXFLAGS   := #e.g., CXXFLAGS=-g -O0 for debugging
LDFLAGS    := $(shell $(PYLON_ROOT)/bin/pylon-config --libs-rpath)
LDFLAGS += `pkg-config --libs opencv`
LDLIBS     := $(shell $(PYLON_ROOT)/bin/pylon-config --libs)
LDLIBS += `pkg-config --libs opencv`

# Rules for building
all: $(NAME1) $(NAME2)

$(NAME1): $(NAME1).o
	$(LD) $(LDFLAGS) -o $@ $^ $(LDLIBS)

$(NAME1).o: $(NAME1).cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

$(NAME2): $(NAME2).o
	$(LD) $(LDFLAGS) -o $@ $^ $(LDLIBS)
   
$(NAME2).o: $(NAME2).cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<


clean:
	$(RM) $(NAME1).o $(NAME1) $(NAME2).o $(NAME2)
