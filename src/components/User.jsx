import { useState } from 'react';
import { useEffect } from 'react';
import { Button, Table } from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

// https://bobbyhadz.com/blog/react-type-usestate-object
// https://medium.com/bb-tutorials-and-thoughts/how-to-make-api-calls-in-react-applications-7758052bf69
function User() {

  const [messages, setMessages] = useState([]);

  async function callFeedback(email) {
    const requestOptions = {
      method: 'POST',
      body: JSON.stringify({ "email": email })
    }

    return await fetch("https://6n45jrbliexwdlyafmybejvuse0abhwk.lambda-url.us-east-1.on.aws/", requestOptions)
      .then(response => response.json()).then(data => {
        // console.log(data);
        return data



        const chats = []

        // setMessages([])

        // data["messages"].map(d => {
        //   setMessages(messages, [...messages, ({
        //     "restaurantOwner": d["restaurantOwner"],
        //     "start": d["messages"][0]["createdAt"],
        //     "end": d["messages"][d["messages"].length - 1]["createdAt"]
        //   })])

        //   chats.push({
        //     "restaurantOwner": d["restaurantOwner"],
        //     "start": d["messages"][0]["createdAt"],
        //     "end": d["messages"][d["messages"].length - 1]["createdAt"]
        //   })
        // })



        // setMessages(chats)

        // console.log(chats)

        // setMessages(chats)


        // console.log(messages)

      })


  }

  useEffect(() => {
    callFeedback(localStorage.getItem("userEmail")).then(data => {
      console.log(data.messages)
      data["messages"].map(d => {
        console.log("insideee")
        // setMessages(d)
      })

      setMessages(data.messages)
      console.log(messages)
    })

  }, []);


  return (
    <div>

      <h1>Profile</h1>



      {/* <Button onClick={submit}>Submit</Button> */}

      {messages && messages.map(row => {
        console.log(row);
          return <h1>{row.restaurantOwner} </h1>
      }
        
      )
      }


    </div>
  );
}

export default User;