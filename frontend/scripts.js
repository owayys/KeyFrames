const GPTResearcher = (() => {
    let socket;
    const init = () => {
        // Not sure, but I think it would be better to add event handlers here instead of in the HTML
        //document.getElementById("startResearch").addEventListener("click", startResearch);
        // document
        //     .getElementById("copyToClipboard")
        //     .addEventListener("click", copyToClipboard);
        document
            .getElementById("sendChatButton")
            .addEventListener("click", sendChatMessage);
        document
            .getElementById("chatInput")
            .addEventListener("keydown", handleChatInput);

        updateState("initial");
    };

    const startResearch = () => {
        document.getElementById("output").innerHTML = "";
        document.getElementById("reportContainer").innerHTML = "";
        updateState("in_progress");

        addAgentResponse({
            output: "🤔 Thinking about research questions for the task...",
        });

        listenToSockEvents();
    };

    const sendChatMessage = () => {
        const chatInput = document.getElementById("chatInput");
        const message = chatInput.value.trim();
        if (message) {
            const requestData = {
                message: message,
            };
            socket.send(`chat ${JSON.stringify(requestData)}`);
            chatInput.value = ""; // Clear the input field after sending the message
            updateState("in_progress");
            const converter = new showdown.Converter();
            const reportContainer = document.getElementById("reportContainer");
            var div = document.createElement("div");
            div.className = "user_response";
            const markdownOutput = converter.makeHtml(message);
            div.innerHTML = markdownOutput;
            reportContainer.appendChild(div);
            updateScroll();
        }
    };

    const handleChatInput = (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendChatMessage();
        }
    };

    const listenToSockEvents = () => {
        const { protocol, host, pathname } = window.location;
        const ws_uri = `${
            protocol === "https:" ? "wss:" : "ws:"
        }//${host}${pathname}ws`;
        const converter = new showdown.Converter();
        socket = new WebSocket(ws_uri);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "logs") {
                addAgentResponse(data);
            } else if (data.type === "report") {
                writeReport(data, converter);
                updateState("finished");
            }
        };

        socket.onopen = (event) => {
            const videoFile = document.querySelector('input[name="video"]')
                .files[0];
            filename = document
                .querySelector('input[name="video"]')
                .value.split("\\")[2];
            const reader = new FileReader();
            reader.onload = (e) => {
                const dataURL = reader.result;
                const base64 = dataURL.slice(dataURL.indexOf(",") + 1);
                const requestData = {
                    name: filename,
                    input: base64,
                };

                socket.send(`start ${JSON.stringify(requestData)}`);
            };
            reader.readAsDataURL(videoFile);
        };
    };

    const addAgentResponse = (data) => {
        const output = document.getElementById("output");
        output.innerHTML +=
            '<div class="agent_response">' + data.output + "</div>";
        output.scrollTop = output.scrollHeight;
        output.style.display = "block";
        updateScroll();
    };

    const writeReport = (data, converter) => {
        console.log(data.output);
        const reportContainer = document.getElementById("reportContainer");
        reportContainer.replaceChildren();
        for (let i = 0; i < data.output.length; i++) {
            var div = document.createElement("div");
            if (data.output[i].role === "AI") {
                div.className = "agent_response";
            } else if (data.output[i].role === "user") {
                div.className = "user_response";
            }
            const markdownOutput = converter.makeHtml(data.output[i].content);
            div.innerHTML = markdownOutput;
            reportContainer.appendChild(div);
        }
        updateScroll();
    };

    const updateScroll = () => {
        window.scrollTo(0, document.body.scrollHeight);
    };

    const copyToClipboard = () => {
        const textarea = document.createElement("textarea");
        textarea.id = "temp_element";
        textarea.style.height = 0;
        document.body.appendChild(textarea);
        textarea.value = document.getElementById("reportContainer").innerText;
        const selector = document.querySelector("#temp_element");
        selector.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
    };

    const setChatInputStatus = (enabled) => {
        const chatInput = document.getElementById("chatInput");
        const sendChatButton = document.getElementById("sendChatButton");

        chatInput.disabled = !enabled;
        sendChatButton.disabled = !enabled;

        if (enabled) {
            chatInput.style.filter = "none";
            sendChatButton.style.filter = "none";
        } else {
            chatInput.style.filter = "opacity(0.3)";
            sendChatButton.style.filter = "opacity(0.3)";
        }
    };

    const updateState = (state) => {
        const chatInput = document.getElementById("chatInput");
        const videoInput = document.getElementById("videoInput");
        const researchButton = document.getElementById("researchButton");

        switch (state) {
            case "in_progress":
                videoInput.disabled = true;
                researchButton.disabled = true;
                setChatInputStatus(false);
                chatInput.placeholder = "Research in progress...";
                break;
            case "finished":
                chatInput.placeholder = "Type something...";
                setChatInputStatus(true);
                break;
            case "error":
                chatInput.placeholder = "Research failed!";
                setChatInputStatus(false);
                break;
            case "initial":
                chatInput.placeholder = "Upload a video to begin...";
                setChatInputStatus(false);
                break;
            default:
                setChatInputStatus(false);
        }
    };

    // const updateState = (state) => {
    //     var status = "";
    //     switch (state) {
    //         case "in_progress":
    //             status = "Research in progress...";
    //             setReportActionsStatus("disabled");
    //             break;
    //         case "finished":
    //             status = "Research finished!";
    //             setReportActionsStatus("enabled");
    //             break;
    //         case "error":
    //             status = "Research failed!";
    //             setReportActionsStatus("disabled");
    //             break;
    //         case "initial":
    //             status = "";
    //             setReportActionsStatus("hidden");
    //             break;
    //         default:
    //             setReportActionsStatus("disabled");
    //     }
    //     document.getElementById("status").innerHTML = status;
    //     if (document.getElementById("status").innerHTML == "") {
    //         document.getElementById("status").style.display = "none";
    //     } else {
    //         document.getElementById("status").style.display = "block";
    //     }
    // };

    // /**
    //  * Shows or hides the download and copy buttons
    //  * @param {str} status Kind of hacky. Takes "enabled", "disabled", or "hidden". "Hidden is same as disabled but also hides the div"
    //  */
    // const setReportActionsStatus = (status) => {
    //     const reportActions = document.getElementById("reportActions");
    //     // Disable everything in reportActions until research is finished

    //     if (status == "enabled") {
    //         reportActions.querySelectorAll("a").forEach((link) => {
    //             link.classList.remove("disabled");
    //             link.removeAttribute("onclick");
    //             reportActions.style.display = "block";
    //         });
    //     } else {
    //         reportActions.querySelectorAll("a").forEach((link) => {
    //             link.classList.add("disabled");
    //             link.setAttribute("onclick", "return false;");
    //         });
    //         if (status == "hidden") {
    //             reportActions.style.display = "none";
    //         }
    //     }
    // };

    document.addEventListener("DOMContentLoaded", init);
    return {
        startResearch,
        copyToClipboard,
    };
})();
