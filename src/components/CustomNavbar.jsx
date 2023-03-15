import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import { Link } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";
import axios from "axios";


function CustomNavbar() {
  const [cookie, setCookie, removeCookie] = useCookies([
    "Email",
    "AccessToken",
    "Customer_Id",
    "State",
    "loginTimestamp",
    "Restaurateur",
    "Type"
  ]);

  let navigate = useNavigate();
  const isState = cookie.State;
  const isRestaurateur = cookie.Restaurateur;

  const LogOut = () => {

    var data = {customerId: cookie.Customer_Id,
      email: cookie.Email,
      loginTimestamp: cookie.loginTimestamp,
      logoutTimestamp: Number(Date.now())}
   
    axios
      .post(
        "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/UserData",
        {
          customerId: cookie.Customer_Id,
          email: cookie.Email,
          loginTimestamp: cookie.loginTimestamp,
          logoutTimestamp: Number(Date.now()),
          status:"LoggedOut"
        }
      )
      .then((res) => {
        console.log(res);
      })
      .catch((error) => {
        console.log(error);
        alert(error);
      });
    removeCookie("Email");
    removeCookie("AccessToken");
    removeCookie("Customer_Id");
    removeCookie("State");
    removeCookie("loginTimestamp");
    removeCookie("Restaurateur");
    removeCookie("Type");
    navigate();
  };

  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand href="#home">Foodie</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            

            {isState ? (
              <>
                <Nav.Link as={Link} onClick={LogOut} to="/login">
                  Logout
                </Nav.Link>
                {/* <Nav.Link as={Link} to="/chat/pr542178@dal.ca">
                  Chat
                </Nav.Link> */}
                
              </>
             
            ) : (
              <>
                <Nav.Link as={Link} to="/login">
                  Login
                </Nav.Link>
                
                <Nav.Link as={Link} to="/user">
                  User
                </Nav.Link>
              </>
            )}

           

            {/* <NavDropdown title="Dropdown" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">
                Another action
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">
                Separated link
              </NavDropdown.Item>
            </NavDropdown> */}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default CustomNavbar;
