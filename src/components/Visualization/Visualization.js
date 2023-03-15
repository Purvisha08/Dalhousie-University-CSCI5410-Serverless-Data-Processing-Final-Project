import React from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Nav from "react-bootstrap/Nav";

const Visualization = () => {
  const userlogs = () => {
    axios.get(
      "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/UserLogs"
    );

    window.open(
      "https://datastudio.google.com/reporting/96487b36-36b6-4c9d-a6da-ef528b4f7cf6"
    );
  };

  const orderlogs = () => {
    axios.get(
      "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/orderLogs"
    );

    window.open(
      "https://datastudio.google.com/reporting/7bb5c5be-00d8-4c79-823d-16c24ede3c79"
    );
  };

  const recipelogs = () => {
    axios.get(
      "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/recipeLogs"
    );

    window.open(
      "https://datastudio.google.com/reporting/798c9d57-f7c3-4934-9d0c-2b504e8dec7c"
    );
  };

  
  return (
    <div className="form-container row">
      {
        localStorage.getItem("Type") == "Restaurateur" ? (
          <>
            <Nav.Item as={Link} to="/data-processing">
              Data Processing
            </Nav.Item>
            <Nav.Item as={Link} to="/polarity">
              Polarity
            </Nav.Item>
            <Nav.Item as={Link} to="/similarity">
                Similarity
              </Nav.Item>
          </>
      
        ) : (
          <></>
        )
      }
      <div className="col-md-6">
        <div className="next-btn">
          {localStorage.getItem("Type") == "Restaurateur" ? (
            <>
              <Nav.Link as={Link} to="/data-processing" style={{ fontSize: 20, paddingBottom: 15 }}>
                Data Processing
              </Nav.Link>
              <Nav.Link as={Link} to="/polarity" style={{ fontSize: 20, paddingBottom: 15 }}>
                Polarity
              </Nav.Link>
            </>
          ) : (
            <></>
          )}
          <center>
            <div className="visualization" style={{ paddingBottom: 15, paddingTop: 30 }}>
              <h3>Visualization</h3>
            </div>
            <div style={{ paddingBottom: 15 }}>
              
              <button
                type="submit"
                className="btn btn-secondary"
                onClick={userlogs}
              >
                User Logs
              </button>
            </div>
            <div style={{ paddingBottom: 15 }}>
              <button
                type="submit"
                className="btn btn-secondary"
                onClick={orderlogs}
              >
                Order Logs
              </button>
            </div>
            <div style={{ paddingBottom: 15 }}>
              <button
                type="submit"
                className="btn btn-secondary"
                onClick={recipelogs}
              >
                Recipe Logs
              </button>
            </div>
          </center>
        </div>
      </div>
    </div>
  );
};
export default Visualization;
