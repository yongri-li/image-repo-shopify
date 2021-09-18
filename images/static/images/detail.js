

//console.log("HELLO")
document.addEventListener('DOMContentLoaded', function () {

    const repo = document.querySelector('#repo-detail')
    const repoID = document.URL.split("/")[document.URL.split("/").length - 1]
    //-----------------------THIS NEEDS TO BE FIXED TO UPLOAD AS WELL--------------------------------------
    fetch(`/repo_details/${repoID}`)
        .then(response => response.json())
        .then(details => {
            console.log(details);
            let title = document.createElement("h2");
            let user = document.createElement("h5");

            let selectOption = document.createElement("select");

            let option0 = document.createElement("option");
            option0.setAttribute("value", "delete")
            option0.innerText = "Delete"

            let option1 = document.createElement("option");
            option1.setAttribute("value", "download")
            option1.innerText = "Download"

            selectOption.append(option0)
            selectOption.append(option1)

            let selected = document.createElement("button");


            selected.innerHTML = `Submit`
            user.innerHTML = `created by ${details.repo.author}`;
            title.innerHTML = details.repo.title;

            repo.append(title);
            repo.append(user);
            repo.append(selectOption);
            repo.append(selected);

            selected.addEventListener('click', function () {

                checks = document.querySelectorAll('input[name="image"]:checked');
                theOption = document.querySelector("select")


                //if(theOption)

                if (theOption.value == "delete") {
                    for (let i = 0; i < checks.length; i++) {
                        fetch(`/delete-image/${details.images[checks[i].id].id}`)
                            .then(response => response.json())
                            .then(ans => {
                                if (i == checks.length - 1) {
                                    location.reload();
                                }
                            })
                    }
                }
                else if (theOption.value == "download") {
                    for (let i = 0; i < checks.length; i++) {


                        let element = document.createElement("a");
                        element.setAttribute('href', details.images[checks[i].id].image);
                        element.setAttribute("download", "download")

                        element.click()
                    }



                }



            })


            imageArray = Object.values(details.images)

            for (let i = 0; i < imageArray.length; i++) {


                let newContent = document.createElement("div");
                newContent.style.borderStyle = "groove";
                newContent.style.margin = "10px";

                let label = document.createElement("label");
                label.setAttribute("for", imageArray[i].title);

                let check = document.createElement("input");
                check.setAttribute("type", "checkbox");
                check.setAttribute("id", imageArray[i].title);
                //check.setAttribute("value","yes");
                check.setAttribute("name", "image");

                label.append(check);
                //label.append(details.images[i].title);



                let title = document.createElement("h3");
                title.innerHTML = imageArray[i].title;

                let newImage = document.createElement("img");
                newImage.setAttribute("src", imageArray[i].image);
                newImage.setAttribute("height", "100");


                newContent.append(title);
                //newContent.append(check);
                newContent.append(label)
                newContent.append(newImage);

                repo.append(newContent);
            }




        })

    //console.log("HEHLDFDF")
    //fetch(`/detail/${repoID}`)


})
