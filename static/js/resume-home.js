document.addEventListener('DOMContentLoaded', function () {

    const mbtiPersonalityTypes = {
        ISTJ: "ISTJs are practical, responsible, and detail-oriented individuals who value tradition and strive for stability.",
        ISFJ: "ISFJs are warm-hearted, compassionate, and conscientious individuals who are dedicated to helping and supporting others.",
        INFJ: "INFJs are insightful, empathetic, and idealistic individuals who are deeply committed to personal growth and making a positive impact on the world.",
        INTJ: "INTJs are strategic, independent, and analytical individuals who possess a strong drive for achieving their goals and implementing their visions.",
        ISTP: "ISTPs are adaptable, logical, and hands-on individuals who excel in troubleshooting and mastering practical skills.",
        ISFP: "ISFPs are gentle, artistic, and sensitive individuals who value personal authenticity and have a deep appreciation for beauty and aesthetics.",
        INFP: "INFPs are compassionate, creative, and introspective individuals who are driven by their values and have a strong desire to make a difference.",
        INTP: "INTPs are curious, logical, and innovative individuals who enjoy exploring complex ideas and theories in depth.",
        ESTP: "ESTPs are energetic, outgoing, and action-oriented individuals who thrive in dynamic environments and enjoy taking risks.",
        ESFP: "ESFPs are spontaneous, fun-loving, and sociable individuals who bring joy and enthusiasm to their interactions and appreciate the present moment.",
        ENFP: "ENFPs are enthusiastic, empathetic, and imaginative individuals who are passionate about inspiring others and exploring new possibilities.",
        ENTP: "ENTPs are quick-witted, innovative, and intellectually curious individuals who enjoy debating ideas and exploring diverse perspectives.",
        ESTJ: "ESTJs are practical, organized, and responsible individuals who value efficiency, structure, and taking charge of situations.",
        ESFJ: "ESFJs are warm, caring, and conscientious individuals who are dedicated to the well-being of others and creating harmonious environments.",
        ENFJ: "ENFJs are charismatic, empathetic, and inspiring individuals who excel at understanding and supporting the needs of others.",
        ENTJ: "ENTJs are assertive, confident, and strategic individuals who are natural leaders and enjoy tackling complex challenges.",
    };

    const modal = new bootstrap.Modal('#jobRecommendationModal', {
        keyboard: false
    })

    function hideProgress() {
        const progressContainer = document.querySelector('.progress-container');
        progressContainer.style.display = 'none';
    }

    function showProgress() {
        const progressContainer = document.querySelector('.progress-container');
        progressContainer.style.display = 'block';
    }

    const fetchData = async function (id) {
        const url = '/sse/?id=' + id;

        const evtSource = new EventSource(url, {
            withCredentials: true,
        });

        evtSource.onmessage = (event) => {
            const newElement = document.createElement("li");
            const eventList = document.getElementById("sse");

            newElement.textContent = `message: ${event.data}`;
            eventList.appendChild(newElement);
        };

        evtSource.addEventListener("error", (event) => {
            // const error = JSON.parse(event.data)
            const error = event.data
            const element = document.getElementById("error-in-modal");
            // element.textContent = error['detail']
            element.textContent = error
        });

        evtSource.addEventListener("prediction", (event) => {
            const prediction = JSON.parse(event.data)
            const mbti = prediction['mbti']

            const divElement = document.getElementById('id40');
            divElement.textContent = mbti

            document.getElementById('id41').textContent = mbtiPersonalityTypes[mbti];
        });

        evtSource.addEventListener("recommendations", (event) => {
            const jobs = JSON.parse(event.data)
            hideProgress()
            document.getElementById('jobTable').style.display = 'table'
            displayJobs(jobs)
            evtSource.close()
        });

        evtSource.addEventListener("ping", (event) => {
            const newElement = document.createElement("li");
            const eventList = document.getElementById("list");
            const time = JSON.parse(event.data).time;
            newElement.textContent = `ping at ${time}`;
            eventList.appendChild(newElement);
        });
    }

    function displayJobs(data) {
        const tableBody = document.getElementById('jobTableBody');
        const modalTitle = document.getElementById('jobModalTitle');
        const modalBody = document.getElementById('jobModalBody');

        // a JavaScript function that takes a string as input, removes newline characters (\n), eliminates extra
        // spaces within the text, and returns the resulting string,
        // ensuring it contains a maximum of 200 characters:
        function processString(inputString) {
            // Ensure maximum of 200 characters
            if (inputString.length > 200) {
                inputString = inputString.substring(0, 200);
                inputString += " ..."
            }

            // Remove newline characters
            let processedString = inputString.replace(/\n/g, '');

            // Remove extra spaces within the text
            processedString = processedString.replace(/ +/g, ' ');

            // Trim leading and trailing spaces
            processedString = processedString.trim();

            return processedString;
        }

        data.forEach((job, index) => {
            const row = document.createElement('tr');
            row.addEventListener('click', () => {
                showModal(job);
            });
            row.style.cursor = 'pointer'

            const titleCell = document.createElement('td');
            titleCell.textContent = job['title'];

            const descriptionCell = document.createElement('td');
            descriptionCell.textContent = processString(job['description']);

            row.appendChild(titleCell);
            row.appendChild(descriptionCell);
            tableBody.appendChild(row);
        });

        function showModal(job) {
            modalTitle.textContent = job['title'];
            modalBody.textContent = job['description'];

            const innerModal = new bootstrap.Modal(document.getElementById('jobModal'));
            innerModal.show();
        }
    }

    function handleClick(event) {
        // Get the clicked element
        const clickedElement = event.currentTarget;

        // Read the attribute value
        const resumeId = clickedElement.getAttribute('data-resume-id');
        const fileName = clickedElement.getAttribute('data-file-name');

        const label = document.getElementById('jobRecommendationModalLabel');
        label.innerText = fileName;

        // Clean the job recommendations table and the predicted personality display
        {
            const el = document.getElementById('jobTableBody');
            el.innerHTML = '';
            document.getElementById('jobTable').style.display = 'none'
            document.getElementById('id40').textContent = ''
        }

        modal.show()

        showProgress()
        fetchData(resumeId).then()
    }

    // Get all elements with the specified class
    const elements = document.querySelectorAll('.resume-card');

    // Attach the onclick listener to each element
    elements.forEach(element => {
        element.addEventListener('click', handleClick);
    });

})
