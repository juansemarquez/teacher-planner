function lockUpdateSchedule(id = null) {
    if(id == null) {
        forms = document.querySelectorAll('.update_schedule')
    }
    else {
        forms = []
        forms.push(document.querySelector('#update_schedule_'+id))
    }
    var j;
    var element;
    for (var i = 0; i < forms.length; i++) {
        for (j=0; j<forms[i].children.length; j++) {
            e = forms[i].children[j]; 
            if (e.tagName == "SELECT" ||
               (e.tagName == "INPUT" && e.type == "text") ) {
                e.readOnly = true;
                continue;
            }
            if (e.tagName == "DIV" && e.classList.contains("lock")) {
                while (e.firstChild) {
                    e.removeChild(e.lastChild);
                }
                let img = document.createElement("img");
                img.src = locked_image;
                img.alt = "Closed lock";
                e.appendChild(img);
                img.addEventListener('click', 
                    function() {unlock(img.parentElement.parentElement);});
                let delete_form = document.querySelector('#delete_schedule_'+forms[i].dataset['id']);
                delete_form.style.display = "none";
            }
        }
    }
}

function unlock(form) {
    // form = document.querySelector('#'+form_id);
    for (j=0; j<form.children.length; j++) {
        e = form.children[j]; 
        if (e.tagName == "SELECT" ||
           (e.tagName == "INPUT" && e.type == "text") ) {
            e.readOnly = false;
            continue;
        }
        if (e.tagName == "DIV" && e.classList.contains("lock")) {
            while (e.firstChild) {
                e.removeChild(e.lastChild);
            }
            let img = document.createElement("img");
            img.src = unlocked_image;
            img.alt = "Open lock";
            img.addEventListener('click', function() {lockUpdateSchedule(form.dataset['id']);});

            let submit = document.createElement("input");
            submit.type="submit";
            submit.value="Update schedule";
            
            let delete_form = document.querySelector('#delete_schedule_'+form.dataset['id']);
            delete_form.style.display = "inline";

            e.appendChild(submit);
            e.appendChild(img);
        }
    }
}


