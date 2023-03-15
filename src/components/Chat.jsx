import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import React, { useEffect, useRef, useState } from 'react';
import './ChatCSS.css';
import firebaseApp from '../Firebase';

import 'firebase/auth';
import 'firebase/analytics';

import { useCollectionData } from 'react-firebase-hooks/firestore';
import { useParams, useSearchParams } from 'react-router-dom';

const CHATMESSAGES_COLLECTION_NAME = "chatMessages"
const CLOUD_FUNCTION_MESSAGE_PUB_SUB_URL = "https://us-central1-serverless-project-370320.cloudfunctions.net/communication_histoty_store"


// const auth = firebaseApp.auth();
const firestore = firebaseApp.firestore();

function Chat() {

  return (
  <div>
    <h1>Chat</h1>
    <ChatRoom></ChatRoom>
  </div>
    
  );
}
const loggedInUser = {type: localStorage.getItem("Type"),userName:localStorage.getItem("userEmail")}
function ChatRoom() {
  var user = {type: localStorage.getItem("Type"),userName:localStorage.getItem("userEmail")}
  
  // const param = useParams()
  var restaurantOwner;
  // var p = `${param.chatId}`
  const [searchParams] = useSearchParams();
  const p = searchParams.get("email")

  if(loggedInUser.type=="User"){
    user = loggedInUser
    restaurantOwner = p
  }
  else{
    restaurantOwner = loggedInUser.userName
    user = {userName:p}
  }
  
  const dummy = useRef();
  const messagesRef = firestore.collection(CHATMESSAGES_COLLECTION_NAME);
  
  
  const query = messagesRef.where("restaurantOwner","==",restaurantOwner)
                .where("userName","==",user.userName)

  const [messages, setMessages] = useState([]);

  useEffect(() => {
    query.onSnapshot(snapshot =>{
      snapshot.forEach((doc) => {
        console.log(doc.id, " => ", doc.data());
        console.log(doc.data()['messages'])
        setMessages(doc.data()['messages'])
        
    });
    })
  },[]);
  

  const [formValue, setFormValue] = useState('');

  const sendMessage = async (e) => {
    e.preventDefault();
    var newMessage = {}
    newMessage = {'message':formValue,createdAt:Date.now(),userName:loggedInUser.userName}
    // https://stackoverflow.com/questions/26505064/what-is-the-best-way-to-add-a-value-to-an-array-in-state
    messages.push(newMessage)
    setMessages(messages)
    
    var chatData = {}
    chatData = {restaurantOwner:restaurantOwner,userName:user.userName,messages:messages}
    await messagesRef.doc(user.userName+"_"+restaurantOwner).set(chatData)

    // https://developer.okta.com/blog/2021/08/02/fix-common-problems-cors
    if(formValue=="solve"){
      fetch(CLOUD_FUNCTION_MESSAGE_PUB_SUB_URL, {
        method : "POST",
        mode: 'no-cors'
      })
      .then((response) => {
        console.log(response)
          if (!response.ok) {
              throw new Error(response.error)
          }
          
          return response.json();
      })
    }

    setFormValue('');
    dummy.current.scrollIntoView({ behavior: 'smooth' });
  }

  return (<>
    <main>

      {messages && messages.map(msg => <ChatMessage key={msg.createdAt} message={msg.message} userName={msg.userName}/>)}

      <span ref={dummy}></span>

    </main>

    <form className='messageform' onSubmit={sendMessage}>

      <input value={formValue} onChange={(e) => setFormValue(e.target.value)} placeholder="Enter message" />

      <button type="submit" disabled={!formValue}>🕊️</button>

    </form>
  </>)
}


function ChatMessage(props) {
  const message= props.message;
  const userName = props.userName
  console.log(props)

  const messageClass = userName === loggedInUser.userName ? 'sent' : 'received';

  return (<>
    <div className={`message ${messageClass}`}>
      <p>{message}</p>
    </div>
  </>)
}

export default Chat;
