//when loaded the page will request comments

function insertComment(comment, commentsDiv){

	commentsDiv.innerHTML = commentsDiv.innerHTML + comment
}

function deleteComment(commentId){
	//confirm delete
	var confirmed = window.confirm("Are you sure you want to delete this comment?");
	if (!confirmed){return;}
	
	//request delete
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200){
			//refresh the comments
			getComments();
		}
	}
	xhttp.open("DELETE","comments/"+commentId+"/");
	xhttp.send();
}

function changeToHideComments(){
	//changes the show/hide button to hide
	var showButton = document.getElementById("showComments");
	showButton.innerHTML = "Hide Comments";
	showButton.setAttribute("onclick", "javascript: hideComments();");
}

function changeToShowComments(){
	//changes the show/hide button to show
	var showButton = document.getElementById("showComments");
	showButton.innerHTML = "Show Comments";
	showButton.setAttribute("onclick", "javascript: showComments();");
}

function hideComments(){
	//hide the comments
	document.getElementById("comments").style.display = "none";
	changeToShowComments();
}

function showComments(){
	//reload the comments and show
	getComments();
	changeToHideComments();
}

function displayMessage(parentElement, messageText){
	var messageDiv = document.createElement("div");
	parentElement.appendChild(messageDiv);
	//<h3>{{messageText}}</h3>
	var h3element = document.createElement("h3");
	var newText = document.createTextNode(messageText);
	h3element.appendChild(newText);
	messageDiv.appendChild(h3element);
}

function insertComments(commentsReply){
	var comments = JSON.parse(commentsReply).comments;
	var numberOfComments = comments.length;
	var commentsDiv = document.getElementById("comments");
	
	//remove all current comments
	while (commentsDiv.firstChild){
		commentsDiv.removeChild(commentsDiv.firstChild);
	}
	//add the new comments
	if (numberOfComments > 0){
		var i;
		for (i = 0; i < numberOfComments; i = i + 1){
			insertComment(comments[i], commentsDiv);
		}
	}
	//show the comments
	commentsDiv.style.display = "block";
	
	//make sure the show/hide button says hide
	changeToHideComments();
	
}

function getComments(){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200){
			insertComments(this.responseText);
		}
	}
	xhttp.open("GET","comments/",true);
	xhttp.send();
}
window.onload = getComments();