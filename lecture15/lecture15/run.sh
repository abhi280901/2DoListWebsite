if ! grep -q FLASK_RUN_PORT ".env" || ! [[ -d vlab ]]; then
    echo Run setup.sh first
    exit 1
fi


app=ajaxdemo

if ! [[ -z $1 ]]; then
    app=$1
fi

# activate the virtual environment for the lecture
source vlab/bin/activate

# run Flask for the lecture
echo Running Flask
FLASK_APP=$app flask run
