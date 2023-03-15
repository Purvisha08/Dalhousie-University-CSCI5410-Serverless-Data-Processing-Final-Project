import "./stylesheet.css";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useCookies } from "react-cookie";
import { useState } from "react";
import { Link } from "react-router-dom";

const Login = () => {
  const [userInformation, setUserInformation] = useState(defaultValues);
  const [cookie, setCookie] = useCookies(["Email", "AccessToken"]);

  const navigate = useNavigate();
  function signin(formValues) {
    setUserInformation(formValues);
    axios
      .post(
        "https://us-central1-csci-5408-w21-352303.cloudfunctions.net/Login",
        {
          ...formValues,
        }
      )
      .then((res) => {
        setCookie("Email", res.data.email);
        localStorage.setItem("userEmail",res.data.email)
        setCookie("AccessToken", res.data.access_token);
        navigate("/SecondFactorAuthentication");
      })
      .catch((error) => {
        alert(error.response.data.error);
      });
  }

  return (
    <Formik
      initialValues={defaultValues}
      validationSchema={SigninValidation}
      onSubmit={signin}
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
                <h3>Sign In</h3>
                <div className="mb-3">
                  <label>Email address</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Enter email"
                    name="email"
                    id="email"
                    value={values.email}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.email && touched.email ? (
                    <span className="error-feedback">{errors.email}</span>
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
                      Next
                    </button>
                    <p className="existing-user text-left">
                      <center>
                        Not a user? <Link to="/signup">sign up</Link>
                      </center>
                    </p>
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

const SigninValidation = Yup.object().shape({
  email: Yup.string().email("Invalid Email").required("Email is required"),
  password: Yup.string().required("Password is required"),
});

const defaultValues = {
  email: "",
  password: "",
};

export default Login;
