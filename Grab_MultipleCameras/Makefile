# Makefile for Basler pylon sample program
.PHONY: all clean

# The program to build
NAME       := Grab_MultipleCameras

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
all: $(NAME)

$(NAME): $(NAME).o
	$(LD) $(LDFLAGS) -o $@ $^ $(LDLIBS)

$(NAME).o: $(NAME).cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

clean:
	$(RM) $(NAME).o $(NAME)
