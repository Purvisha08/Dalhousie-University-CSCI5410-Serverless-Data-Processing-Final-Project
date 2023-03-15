import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import axios from "axios";
import { useCookies } from "react-cookie";
import { Link } from "react-router-dom";

function Home() {
  const [cookies, setCookies] = useCookies([
    "Type",
    "loginTimestamp",
    "Customer_Id",
  ]);

  return (
    <div>
      {
              localStorage.getItem("Type") == "User" ? (
                <>
                  <Nav.Item as={Link} to="/user">
                    User Profile
                  </Nav.Item>
                </>

              ) : (
                <></>
              )
            }
    </div>
  );
}

export default Home;
