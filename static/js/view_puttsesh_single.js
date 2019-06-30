deleteButtons = document.querySelectorAll('.delete-button');

deleteButtons.forEach(function (deleteButton) {
    deleteButton.addEventListener('click', function () {
        // First, hide the original delete button.
        deleteButton.style.display = 'none'

        // Then create lots of helpful variables.
        // The first 3 are new elements to decorate our page.
        var delForm = document.createElement('form'),
            delFormButton = document.createElement('input'),
            delFormLabel = document.createElement('label');



        // Then retrieve some necessary information, including the parent
        // element of the clicked button and that parent element's innerText.
        var parentEl = deleteButton.parentElement,
            delButtonInner = deleteButton.innerText;

        // Create and populate delForm with a button and label.
        delFormButton.setAttribute('type', 'submit')
        delFormButton.setAttribute('value', delButtonInner)
        delFormButton.classList.add('delete-button')

        delFormLabel.innerText = 'Are you sure?'
        delFormLabel.appendChild(delFormButton)

        delForm.appendChild(delFormLabel)
        delForm.setAttribute('method', 'POST')


        // Then, depending on whether user is deleting a putt or a putting
        // session we'll populate the generated form with the requisite data.
        if (delButtonInner === 'Delete Putt') {
            var hiddenPuttId = document.createElement('input'),
                puttId = parentEl.getAttribute('putt-id');
            hiddenPuttId.style.display = 'none'
            hiddenPuttId.setAttribute('type', 'text')
            hiddenPuttId.setAttribute('name', 'putt-id')
            hiddenPuttId.setAttribute('value', puttId)

            delForm.appendChild(hiddenPuttId)
        } else {
            var puttseshId = parentEl.getAttribute('puttsesh-id'),
                hiddenSeshId = document.createElement('input')

            hiddenSeshId.style.display = 'none'
            hiddenSeshId.setAttribute('type', 'text')
            hiddenSeshId.setAttribute('value', puttseshId)
            hiddenSeshId.setAttribute('name', 'puttsesh-id')

            delForm.appendChild(hiddenSeshId)
        }

        parentEl.appendChild(delForm)
    })
})