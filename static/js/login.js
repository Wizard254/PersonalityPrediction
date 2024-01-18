document.addEventListener('DOMContentLoaded', function () {

    function wrapAndAppendElements(elementId, classDict) {
        const element = document.getElementById(elementId);
        if (element) {
            const parent = element.parentNode;

            const newDiv = document.createElement("div");
            newDiv.className = classDict['div'];
            newDiv.appendChild(element);
            const i = document.createElement("i");
            i.className = classDict['i'];
            newDiv.appendChild(i);

            parent.parentNode.replaceChild(newDiv, parent);
        }
    }

    function deleteLabels(elementIds) {
        elementIds.forEach(function (elementId) {
            const labels = document.querySelectorAll("label[for='" + elementId + "']");
            labels.forEach(function (label) {
                label.remove();
            });
        });
    }

    function addClassToSubmitButton(clazz) {
        const submitButton = document.querySelector("button[type='submit']");
        if (submitButton) {
            clazz.forEach(function (c) {
                submitButton.classList.add(c);
            })
        }
    }

    function moveElement(elementId, newParentId) {
        const element = document.getElementById(elementId);
        const newParent = document.getElementById(newParentId);

        if (element && newParent) {
            newParent.appendChild(element);
        }
    }

    function swapChildElements(parent) {
        if (parent && parent.children.length >= 2) {
            const firstChild = parent.children[0];
            const secondChild = parent.children[1];

            parent.insertBefore(secondChild, firstChild);
        }
    }

    const forgotElement = document.getElementById('id_password_helptext')
    const rem = document.getElementById('id_remember')
    const rem_p = rem.parentElement
    rem_p.className = 'remember-forgot'
    rem_p.children[0].textContent = ' Remember Me'

    rem_p.appendChild(forgotElement)
    swapChildElements(rem_p)

    forgotElement.children[0].textContent = 'Forgot password?'

    rem_p.children[2].className = 'align-end'

    function wrapFirstTwoChildren(parentElement) {
        if (parentElement && parentElement.children.length >= 2) {
            const firstChild = parentElement.children[0];
            const secondChild = parentElement.children[1];

            const newDiv = document.createElement("div");
            newDiv.appendChild(firstChild);
            newDiv.appendChild(secondChild);
            newDiv.className = 'align-start'

            parentElement.insertBefore(newDiv, parentElement.firstChild);
        }
    }
    wrapFirstTwoChildren(rem_p)

    wrapAndAppendElements('id_login', {'div': 'input-box', 'i': 'bx bxs-user'})
    wrapAndAppendElements('id_password', {'div': 'input-box', 'i': 'bx bxs-lock-alt'})

    deleteLabels(['id_login', 'id_password'])
    addClassToSubmitButton(['btn'])

})
