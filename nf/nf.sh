#!/bin/bash

CONFIG="$HOME/.config/nf"
DEST='.'
TYPE=''
NAME=''
EXT=''
FORCE=0

usage() {
  echo nf TYPE [-p DEST] >&2 
  exit 1
}

verify_env() {
  [ -z $NAME ] && {
    echo File name is empty. Please specify a name.
    exit 1
  }
}

new_dir() {
  DEST="$DEST/$1"
  [ -d $DEST ] && {
    echo Directory $DEST already exists...
    exit 1
  }
  mkdir $DEST
}

new_file() {
  touch $1
}

populate_file() {
  if [ -n "$2" ]
  then
    [ -f $CONFIG/$2 ] && {
      out=$($CONFIG/$2 $NAME)
      echo "$out" >> $1
    }
  else
    [ -f $CONFIG/$TYPE ] && {
      out=$($CONFIG/$TYPE $NAME)
      echo "$out" >> $1
    }
  fi
}

while getopts ":hfp:" o;
do
  case "$o" in
    h) 
      usage
      ;;
    f)
      FORCE=1
      ;;
    p)
      DEST=$OPTARG
      ;;
  esac
done
NAME=${@:$OPTIND+1:1}
TYPE="${@:$OPTIND:1}"

case "$TYPE" in 
  html)
    EXT=".html"
    ;;
  css)
    EXT=".css"
    ;;
  js)
    EXT=".js"
    ;;
  jsx)
    EXT=".js"
    new_dir $NAME
    new_file "$DEST/$NAME.module.css"
    populate_file "$DEST/$NAME.module.css" "css"
    ;;
  h)
    EXT=".h"
    ;;
  hh|h++|hpp|hxx)
    EXT=".hpp"
    ;;
  c)
    EXT=".c"
    ;;
  cc|c++|cxx|cpp)
    EXT=".cpp"
    ;;
  sh)
    EXT=".sh"
    ;;
  py)
    EXT=".py"
    ;;
  *)
    usage
    ;;
esac

new_file "$DEST/$NAME$EXT"
populate_file "$DEST/$NAME$EXT"

if [ "$TYPE" == "sh" ]
then
  chmod +x "$DEST/$NAME$EXT"
fi
