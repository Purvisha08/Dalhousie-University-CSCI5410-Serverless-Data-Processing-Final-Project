import "./stylesheet.css";
import { Formik, Form } from "formik";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useCookies } from "react-cookie";
import { useState } from "react";

function decodeText() {
  var dedodedText = "";
  var allowedCharacters = "abcdefghijklmnopqrstuvwxyz";

  for (var i = 0; i < 6; i++)
    dedodedText =
      dedodedText +
      allowedCharacters.charAt(
        Math.floor(Math.random() * allowedCharacters.length)
      );

  return dedodedText;
}

const TEXT = decodeText();

const ThirdFactorAuthentication = () => {
  const [decodedText, setDecodedText] = useState(defaultValues);
  const [cookies, setCookies] = useCookies([
    "State",
    "loginTimestamp",
    "Customer_Id",
    "Type",
  ]);

  const navigate = useNavigate();
  const signupForm = (formValues) => {
    axios
      .post(
        "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/ThirdFactorAuth",
        {
          text: TEXT,
          decoded: decodedText,
          customerId: cookies.Customer_Id,
        }
      )
      .then((res) => {
        setCookies("State", res.data.state);
        setCookies("Type", res.data.type);
        localStorage.setItem("Type", res.data.type);
        if (res.data.state == false) {
          alert("Cipher Mismatched");
        } else {
          setCookies("loginTimestamp", Number(Date.now()));
          
          localStorage.setItem("id", cookies.Customer_Id)
          

          axios
          .post(
            "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/UserData",
            {
              customerId: cookies.Customer_Id,
              email: cookies.Email,
              loginTimestamp: Number(Date.now()),
              logoutTimestamp:"",
              status:"LoggedIn"
            }
          )
          .then((res) => {
            console.log(res);
          })
          .catch((error) => {
            console.log(error);
            alert(error);
          });

          if (res.data.type == "User") {
            navigate("/");
          } else {
            navigate("/visualization");
          }
        }
      })
      .catch((error) => {
        alert(error);
      });
  };

  return (
    <Formik initialValues={defaultValues} onSubmit={signupForm}>
      {(formik) => {
        const { handleSubmit, handleBlur } = formik;

        return (
          <div className="form-container row">
            <div className="col-md-6 form">
              <Form onSubmit={handleSubmit}>
                <h3>Third Factor Authentication</h3>
                <div className="mb-2">
                  <label>Cipher String</label>
                  <input
                    type="text"
                    className="form-control"
                    name="cipher-string"
                    id="cipher-string"
                    value={TEXT}
                    disabled
                  />
                </div>
                <div className="mb-2">
                  <label>Decoded Text</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Enter decoded text"
                    name="decodedText"
                    id="decodedText"
                    value={decodedText.decoded}
                    onBlur={handleBlur}
                    onChange={(e) => setDecodedText(e.target.value)}
                  />
                </div>
                <div className="d-grid pt-2">
                  <center>
                    <button type="submit" className="btn btn-secondary">
                      Sign In
                    </button>
                  </center>
                </div>
              </Form>
            </div>
          </div>
        );
      }}
    </Formik>
  );
};

const defaultValues = {
  decoded: "",
};

export default ThirdFactorAuthentication;
