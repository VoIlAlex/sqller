#!/bin/bash

while 1
do
  echo "Do you want to push all? [y/n]"
  read $ANSWER
  if [ $ANDSWER = 'y' ]
  then
    break
  fi
  elif [ $ANSWER = 'n' ]
  then
    exit 0
  fi
done

git push
git push origin --tags
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*