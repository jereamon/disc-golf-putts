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


function createUpdateForm(noPutters, puttId) {
    /** Creates and populates a form with the necessary inputs and classese
     * to enable async updating of Putt.putts_made.
     */
    updateForm = document.createElement('form');
    updateButton = document.createElement('button');
    selectInput = document.createElement('select');

    selectInput.classList.add("update-select" + puttId)

    updateButton.classList.add('gen-update-button');
    updateButton.innerText = 'Update';
    updateButton.setAttribute('type', 'button');

    for (var i = 0; i < parseInt(noPutters)+1; i++) {
        option = document.createElement('option')
        option.innerText = i
        selectInput.appendChild(option)
    };

    updateForm.appendChild(selectInput);
    updateForm.appendChild(updateButton);

    updateForm.setAttribute('role', 'form');
    updateForm.classList.add('update-form-' + puttId);

    return updateForm
}


$(function () {
    $('.edit-button').click(function () {
        var puttId = $(this).parent().attr('putt-id'),
            noPutters = $('.no_putters').text();

        $(this).parent().next('div').css('display', 'none')
        $(this).css('display', 'none')

        updateForm = createUpdateForm(noPutters, puttId)
        $(this).parent().append(updateForm);

        $('.gen-update-button').click(function () {
            // Had to save these here because inside $.ajax 'this' == the ajax
            // function.
            // These are the two elements that were set to display='none' above.
            var thisDeleteDiv = $(this).parent().parent().next('div'),
                thisEditButton = $(this).parent().prev(),
                thisEditContainer = $(this).parent().parent(),
                thisParentPuttContainer = $(this).parent().parent().parent();

            $.ajax({
                url: '/update_putt',
                data: {
                    'new_value': $('.update-select' + puttId).val(),
                    'putt_id': puttId,
                    'no_putters': noPutters
                },
                type: "POST",
                success: function (response) {
                    console.log(response)

                    parsed_response = JSON.parse(response)
                    $('.putts-made-' + puttId).text(parsed_response['new_value'])

                    tempP = document.createElement('p')
                    tempP.innerText = 'Putt Updated!'
                    tempP.setAttribute('style', 'font-size: 2rem; text-align: center;')

                    thisEditContainer.append(tempP)

                    thisParentPuttContainer.css('background', '#009900')
                    setTimeout(function () {
                        tempP.remove()
                        thisDeleteDiv.css('display', 'block')
                        thisEditButton.css('display', 'block')
                        thisParentPuttContainer.css('background', 'none')
                    }, 2500)


                    updateForm.remove()
                },
                error: function (error) {
                    console.log(error)
                }
            })
        })
    })
})