function displayMessage(parentElement, messageText){
	var messageDiv = document.createElement("div");
	parentElement.appendChild(messageDiv);
	//<h3>{{messageText}}</h3>
	var h3element = document.createElement("h3");
	var newText = document.createTextNode(messageText);
	h3element.appendChild(newText);
	messageDiv.appendChild(h3element);
}

function add_to_list(list, to_add){
	var li = document.createElement("li");
	li.appendChild(to_add);
	list.appendChild(li);
}


function newAuthorLink(parentDiv, user){
	var newlink = document.createElement("a");
	var newtext = document.createTextNode(user.name);
	newlink.className ="projectDescriptor";
	newlink.appendChild(newtext);
	var url = "/muse/users/";
	url = url + user.id + "/";
	newlink.setAttribute("href", url);//link to authors Page
	return newlink;
}

function newProjectLink(parentDiv, projectName, projectSlug, isLoggedIn){
	var newlink = document.createElement("a");
	var newtext = document.createTextNode(projectName);
	newlink.className ="projectDescriptor";
	newlink.className += " projectNameLink";
	newlink.appendChild(newtext);
	if (isLoggedIn){
		var url = "/muse/projects/";
		url = url + projectSlug + "/";
		newlink.setAttribute("href",url);//link to projectPage
	}
	return newlink;
}


function insertProjectPreviews(inputDict){
	
	//alert(JSON.stringify(inputDict));

	var isLoggedIn = inputDict.SignedIn;
	var projectPreviews = inputDict.ProjectPreviews;
	var numberOfPreviews = projectPreviews.length;
	var projectPreviewsBlock = document.getElementById("projectPreviews");
	var i;
	
	if (numberOfPreviews == 0){
		
		displayMessage(projectPreviewsBlock, "No projects")
	}

	for (i = 0; i < numberOfPreviews; i = i + 1){
		
		projectPreview = projectPreviews[i];
		addProjectPreview(projectPreview, projectPreviewsBlock, isLoggedIn);
	}

}

function addProjectPreview(projectPreview, parentDiv, isLoggedIn){
	
	//var tempElement;
	//var tempText;
	var previewDiv = document.createElement("div");
	var list = document.createElement("ul");
	previewDiv.className ="projectPreview";
	previewDiv.innerHTML = projectPreview;
	
	// previewDiv.id ="projectReview"+projectPreview.nameSlug;
	
	// add_to_list(list,newProjectLink(previewDiv, projectPreview.name, projectPreview.slug, isLoggedIn));
	// //tempElement = document.createElement("h3");
	// //tempText = document.createTextNode(projectPreview.name);
	// //tempElement.appendChild(tempText);
	// //previewDiv.appendChild(tempElement);
	
	// add_to_list(list,newAuthorLink(previewDiv, projectPreview.Author));
	// //tempElement = document.createElement("p");
	// //tempText = document.createTextNode(projectPreview.Author.name);
	// //tempElement.appendChild(tempText);
	// //previewDiv.appendChild(tempElement);
	
	// //tempElement = document.createElement("p");
	// //tempText = document.createTextNode(projectPreview.genre);
	// //tempElement.className ="projectDescriptor";
	// //tempElement.appendChild(tempText);
	// //add_to_list(list,tempElement);
	
	// tempElement = document.createElement("p");
	// tempText = document.createTextNode("Comments - " + projectPreview.NumberOfComments);
	// tempElement.className ="projectDescriptor";
	// tempElement.appendChild(tempText);
	// add_to_list(list,tempElement);
	
	// //tempElement = document.createElement("p");
	// //tempText = document.createTextNode(projectPreview.PageDescription);
	// //tempElement.className ="projectDescriptor";
	// //tempElement.appendChild(tempText);
	// //add_to_list(list,tempElement);
	
	// previewDiv.appendChild(list);
	// addProjectPreviewAccessButtons(previewDiv, isLoggedIn, projectPreview.canEdit, projectPreview.slug);
	
	parentDiv.appendChild(previewDiv);
}

function addProjectPreviewAccessButtons(previewDiv, isLoggedIn, canEdit, slug){
	var tempElement;
	var tempText;
	var divBlock = document.createElement("div");
	divBlock.className = "projectPreviewAccessButtons";
	previewDiv.appendChild(divBlock);
	if(isLoggedIn){
		
		//View button
		tempElement = document.createElement("button");
		tempText = document.createTextNode("View");
		tempElement.appendChild(tempText);
		var eventString = "javascript: location.assign('/muse/projects/";
		eventString = eventString + slug + "/')";
		tempElement.setAttribute("onclick", eventString);//link to projectPage
		divBlock.appendChild(tempElement);
		
		if (canEdit){
			
			//Edit button
			//tempElement = document.createElement("button");
			//tempText = document.createTextNode("Edit");
			//tempElement.appendChild(tempText);
			//add edit event!!! Should either be link to edit page or load in the project and display with edit controls
			//divBlock.appendChild(tempElement);
			
			//Delete button
			tempElement = document.createElement("button");
			tempText = document.createTextNode("Delete");
			tempElement.appendChild(tempText);
			var eventString = "javascript: deleteProject('";
			eventString = eventString + slug + "')";
			tempElement.setAttribute("onclick", eventString);
			
			//add delete event!!! Should ask if user wants to delete then request server to delete
			divBlock.appendChild(tempElement);
		}
		
	}
	else{
	//LoginToView button
	var newlink = document.createElement("a");
	tempText = document.createTextNode("Log In To View");
	newlink.appendChild(tempText);
	newlink.className ="projectDescriptor";
	newlink.setAttribute("href","/muse/login/");//link to login page
	divBlock.appendChild(newlink);
	}
}

function deleteProject(projectSlug){
	//confirm delete
	var confirmed = window.confirm("Are you sure you want to delete this project?");
	if (!confirmed){return;}
	
	//request delete
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200){
			var deleted = document.getElementById("projectPreview" + projectSlug);
			deleted.parentNode.removeChild(deleted);
		}
	}
	xhttp.open("DELETE","/muse/projects/"+projectSlug+"/");
	xhttp.send();
}

//functionChangeLoggedIn

function getProjectPreviews(){
	//change to request from server
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200){
			//alert(this.responseText);
			insertProjectPreviews(JSON.parse(this.responseText));
		}
	}
	// get user_id
	var user_id = -1;
	var url = window.location.pathname.split('/');
	//alert (url);
	//alert (url.length == 5);
	//alert (url[1]);
	//alert (url[2]);
	//alert (url[3]);
	var number;
	if (url.length == 5 && url[1] == "muse" && url[2] == "users"){
		user_id = url[3];
		number = 0;//get all of a users projects
	}
	else{
		number = 5;
	}
	
	
	
	xhttp.open("GET","/muse/projects/?user_id="+user_id+"&number=" + number,true);
	xhttp.send();
}

function reloadProjectPreviews(){
	
	var projectPreviewsBlock = document.getElementById("projectPreviews");
	
	//clear current previews
	while (projectPreviewsBlock.firstChild){
		projectPreviewsBlock.removeChild(projectPreviewsBlock.firstChild);
	}
	
	//load new previews
	getProjectPreviews();
}

function onPageLoad(isLoggedIn, username, projectAuthor){
	
	getProjectPreviews();
	}
	
window.onload = onPageLoad(); 

