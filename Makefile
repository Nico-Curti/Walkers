# Walkers Version
MAJOR 	 := 1
MINOR 	 := 0
REVISION := 0

# Setting bash colors
RED    := $(shell tput -Txterm setaf 1)
YELLOW := $(shell tput -Txterm setaf 3)
GREEN  := $(shell tput -Txterm setaf 2)
PURPLE := $(shell tput -Txterm setaf 5)
WHITE  := $(shell tput -Txterm setaf 9)
LBLUE  := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0   )

#################################################################
#                         COMPILE OPTIONS                       #
#################################################################

OMP     ?= 1
DEBUG   ?= 1
VERBOSE ?= 1

STD     := -std=c++17

CFLAGS  := -DMAJOR=$(MAJOR) -DMINOR=$(MINOR) -DREVISION=$(REVISION)
#-Wall -Wextra -Wno-unused-result
LDFLAGS := -fPIC -lGL -lGLU -lglut

#################################################################
#                         PARSE OPTIONS                         #
#################################################################

define config
	$(if $(filter $(1), $(2)), $(3), $(4) )
endef

ifneq ($(STD), -std=c++17)
$(error $(RED)C++ minimum standard required is c++17$(RESET))
endif

omp_check := $(shell echo |cpp -fopenmp -dM | grep -i open | cut -d' ' -f 3)
ifneq ($(shell expr $(omp_check) \>= 201307), 1)
$(error $(RED)Your OpenMP is too old. Required OpenMP 4.0. Please upgrade.$(RESET))
endif

CFLAGS  += $(strip $(call config, $(OMP),     1, -fopenmp, ))
CFLAGS  += $(strip $(call config, $(VERBOSE), 1, -DVERBOSE,))
OPTS    := $(strip $(call config, $(DEBUG),   1, -O0 -g -DDEBUG, -Ofast))

#################################################################
#                         SETTING DIRECTORIES                   #
#################################################################

HPP_DIR    := ./cpp/src
INC_DIR    := ./cpp/include
EXAMPLE    := ./example
VIEWER_DIR := $(INC_DIR)/viewer
OBJ_DIR    := ./obj
OUT_DIR    := ./bin
DEP_DIR    := ./.dep

DFLAGS  = -MT $@ -MMD -MP -MF $(DEP_DIR)/$*.Td

HPP    := $(sort $(wildcard $(HPP_DIR)/*.hpp))
VIEW   := $(sort $(wildcard $(HPP_DIR)/viewer/*.cpp))
SRC    := $(HPP) $(VIEW)
HEADER := $(sort $(wildcard $(INC_DIR)/*.h))
HEADER += $(sort $(wildcard $(INC_DIR)/viewer/*h))
EXE    := $(sort $(wildcard $(EXAMPLE)/*.cpp))
INC    := -I$(INC_DIR) -I$(HPP_DIR) -I$(VIEWER_DIR)

OBJS   := $(patsubst $(HPP_DIR)/viewer/%.cpp, $(OBJ_DIR)/%.o, $(VIEW))
HPPo   := $(patsubst $(HPP_DIR)/%.hpp, $(OBJ_DIR)/%.o, $(HPP))

#################################################################
#                         OS FUNCTIONS                          #
#################################################################

define MKDIR
	$(if $(filter $(OS), Windows_NT), mkdir $(subst /,\,$(1)) > nul 2>&1 || (exit 0), mkdir -p $(1) )
endef

mkdir_dep  := $(call MKDIR, $(DEP_DIR))
mkdir_obj  := $(call MKDIR, $(OBJ_DIR))
mkdir_out  := $(call MKDIR, $(OUT_DIR))

#################################################################
#                         BUILD COMMAND LINE                    #
#################################################################

CFLAGS += $(STD)
CFLAGS += $(OPTS)
CFLAGS += $(INC)

all: help

#################################################################
#                         MAIN RULES                            #
#################################################################

test: $(DEP_DIR) $(OBJ_DIR) $(OUT_DIR) $(OBJS)       ##@examples Build test example.
	@printf "%-80s " "Building test example ..."
	@$(CXX) $(OBJS) $(EXAMPLE)/run.cpp -o $(OUT_DIR)/run $(CFLAGS) $(LDFLAGS)
	@printf "[done]\n"


#################################################################
#                         walkers  RULES                        #
#################################################################

build: $(DEP_DIR) $(OBJ_DIR) $(OBJS) $(HPPo)         ##@library Build all the scripts.

$(OBJ_DIR)/%.o: $(HPP_DIR)/viewer/%.cpp $(DEP_DIR)/%.d # compile all hpp in HPP_DIR for OBJ
	@printf "%-80s " "generating obj for $<"
	@$(CXX) $(DFLAGS) $(CFLAGS) -c $< -o $@
	@mv -f $(DEP_DIR)/$*.Td $(DEP_DIR)/$*.d && touch $@
	@printf "[done]\n"

$(OBJ_DIR)/%.o: $(HPP_DIR)/%.hpp $(DEP_DIR)/%.d # compile all hpp in HPP_DIR for OBJ
	@printf "%-80s " "generating obj for $<"
	@$(CXX) $(DFLAGS) $(CFLAGS) -c $< -o $@
	@mv -f $(DEP_DIR)/$*.Td $(DEP_DIR)/$*.d && touch $@
	@printf "[done]\n"

$(DEP_DIR)/%.d: ;
.PRECIOUS: $(DEP_DIR)/%.d
include $(wildcard $(patsubst %,$(DEP_DIR)/%.d,$(basename $(VIEW))))

#################################################################
#                         UTILS RULES                           #
#################################################################

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
# A category can be added with @category
HELP_FUN = \
	%help; \
	while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
	print "\t\t\t$(LBLUE)Walkers Makefile$(RESET)\n"; \
	print "usage: ${PURPLE}make${RESET} ${GREEN}<target>${RESET}\n\n"; \
	for (sort keys %help) { \
	print "${WHITE}$$_:${RESET}\n"; \
	for (@{$$help{$$_}}) { \
	$$sep = " " x (32 - length $$_->[0]); \
	print "  ${PURPLE}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
	}; \
	print "\n"; }
.PHONY: clean

help:                   ##@utils Show this help message.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

clean:                  ##@utils Clean all files.
	@printf "%-80s " "Cleaning all files..."
	@rm -rf $(OBJS) $(ALIB) $(SLIB) $(OBJ_DIR)/* $(DEP_DIR)/*
	@printf "[done]\n"
$(DEP_DIR):             ##@utils Make dependencies directory.
	@printf "%-80s " "Creating dependencies directory ..."
	@$(mkdir_dep)
	@printf "[done]\n"
$(OBJ_DIR):             ##@utils Make objs directory.
	@printf "%-80s " "Creating objs directory ..."
	@$(mkdir_obj)
	@printf "[done]\n"
$(OUT_DIR):             ##@utils Make output (executables) directory.
	@printf "%-80s " "Creating output directory ..."
	@$(mkdir_out)
	@printf "[done]\n"
