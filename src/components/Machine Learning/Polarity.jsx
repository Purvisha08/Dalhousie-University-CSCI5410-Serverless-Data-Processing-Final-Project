






import { useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

// https://bobbyhadz.com/blog/react-type-usestate-object
// https://medium.com/bb-tutorials-and-thoughts/how-to-make-api-calls-in-react-applications-7758052bf69

function Polarity() {


    useEffect(() => {


        async function callFeedback(restaurantId){
            const requestOptions = {
                method: 'POST',
                body: JSON.stringify({"restaurantId": restaurantId})
            }
        
            const response = await fetch("https://blrahm4y2inrhctbpjh5uojgoq0geuob.lambda-url.us-east-1.on.aws/", requestOptions)
                .then(response => response.json()).then(data => alert("You will get update results in some time"))
        } 

        callFeedback(localStorage.getItem("id"))

        
    }, [])

  return (
    <div>
        <iframe width="1000" height="750" src="https://datastudio.google.com/embed/reporting/9172c53f-90b0-46a5-9d12-986157bf5d26/page/6sW9C"></iframe>
    </div>
    
  );
}

export default Polarity;