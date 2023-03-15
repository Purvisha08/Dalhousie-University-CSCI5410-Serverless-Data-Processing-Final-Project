
import axios from 'axios';
import { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { useForm } from 'react-hook-form';
import { Form } from 'semantic-ui-react';

// https://bobbyhadz.com/blog/react-type-usestate-object

function Similarity() {

    const { register, handleSubmit, reset, formState: { errors } } = useForm();

    const [response, setResponse] = useState(null);


    const onSubmit = (data) => {

        async function callFeedback(restaurantId) {

            axios.post("https://us-central1-serverless-project-370320.cloudfunctions.net/automl", {
                "first": data.first,
                "second": data.second
            })
                .then(response => setResponse(response.data))

                console.log(response)
        }

        callFeedback(localStorage.getItem("id"))

    }

    return (
        <div>
            <Form onSubmit={handleSubmit(onSubmit)}>
                <Form.Field>
                    {/* <label>Choose File</label> */}
                    <input placeholder='Enter First Recipe' type="text" {...register('first', { required: true })} />
                    <input placeholder='Enter Second Recipe' type="text" {...register('second', { required: true })} />
                </Form.Field>
                <Button type='submit'>Submit</Button>
            </Form>
            
            {
                response != null ? response.similar ?(<h5> Recipes are  similar with similarity {response.similarity}</h5>):(<h5> Recipes are not similar with similarity {response.similarity}</h5>) : <h5></h5>

            }
        </div>

    );
}

export default Similarity;