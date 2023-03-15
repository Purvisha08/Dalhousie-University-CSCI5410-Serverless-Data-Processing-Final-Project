import { useState } from "react";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useCookies } from "react-cookie";

const RestaurateurLogin = () => {
  const [restaurateurDetails, setRestaurateurDetails] = useState(defaultValues);
  const [cookie, setCookie, removeCookie] = useCookies([
    "Email",
    "AccessToken",
    "Customer_Id",
    "Restaurateur",
    "loginTimestamp",
  ]);

  const navigate = useNavigate();

  const restaurateurForm = (formValues) => {
    setRestaurateurDetails(formValues);
    axios
      .post(
        "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/RestaurateurLogin",
        {
          ...formValues,
        }
      )
      .then((res) => {
        console.log(res);
        setCookie("Restaurateur", true);
        removeCookie("Email");
        removeCookie("AccessToken");
        removeCookie("Customer_Id");
        removeCookie("State");
        removeCookie("loginTimestamp");
        navigate("/visualization");
      })
      .catch((error) => {
        console.log(error);
        alert("Invalid Credentials.");
      });
  };

  return (
    <Formik
      initialValues={defaultValues}
      validationSchema={restaurateurFormValidation}
      onSubmit={restaurateurForm}
    >
      {(formik) => {
        const {
          values,
          errors,
          touched,
          isValid,
          dirty,
          handleChange,
          handleSubmit,
          handleBlur,
        } = formik;
        return (
          <div className="form-container row">
            <div className="col-md-6 form">
              <Form onSubmit={handleSubmit}>
                <h3>Restaurateur Sign In</h3>
                <div className="mb-3">
                  <label>Username</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Enter Username"
                    name="username"
                    id="username"
                    value={values.username}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.username && touched.username ? (
                    <span className="error-feedback">{errors.username}</span>
                  ) : null}
                </div>

                <div className="mb-3">
                  <label>Password</label>
                  <input
                    type="password"
                    className="form-control"
                    placeholder="Enter password"
                    name="password"
                    id="password"
                    value={values.password}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                </div>
                <div className="d-grid">
                  <center>
                    <button
                      type="submit"
                      className="btn btn-secondary"
                      disabled={!(dirty && isValid)}
                    >
                      Login
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

const restaurateurFormValidation = Yup.object().shape({
  username: Yup.string().required("Username is required"),
  password: Yup.string().required("Password is required"),
});

const defaultValues = {
  username: "",
  password: "",
};

export default RestaurateurLogin;
