#!/bin/bash

while [ 1 = 1 ]
do
  read -p "Do you want to push all? [y/n] "  ANSWER
  if [ $ANSWER = "y" ]
  then
    break
    elif [ $ANSWER = "n" ]
    then
      exit 0
  fi
done

git push
git push origin --tags
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*