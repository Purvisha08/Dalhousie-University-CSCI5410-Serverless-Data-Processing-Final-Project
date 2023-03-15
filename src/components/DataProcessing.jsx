import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
// import Table from 'react-bootstrap/Table';
import { Table } from 'semantic-ui-react'
import {Button,Modal} from 'react-bootstrap'
import { uploadRecipe, putRecipeData, fetchRecipeData, extractData, updateRecipe } from '../services/Recipe';
import { Form } from 'semantic-ui-react';
import React, { createRef, useEffect, useRef, useState } from 'react';
import { useForm } from 'react-hook-form';
import { v4 as uuid } from 'uuid';
import { useCookies } from "react-cookie";

// https://www.freecodecamp.org/news/how-to-perform-crud-operations-using-react/
// https://bobbyhadz.com/blog/react-type-usestate-object
// https://stackoverflow.com/questions/53824116/react-hooks-usestate-array
// https://www.folkstalk.com/tech/react-form-reload-page-with-code-examples/
// https://www.npmjs.com/package/react-uuid

function DataProcessing() {


    const hiddenInputFile = React.useRef(null);

    const { register, handleSubmit, reset, formState: { errors } } = useForm();

    const [state, setState] = useState({ "fileUpload": "", "createRecipe": 0 });

    const fileUploadRef = createRef();
    const [cookies, setCookies] = useCookies(["State", "loginTimestamp", "Customer_Id"]);

    const [recipeObj,setRecipeObj] = useState(null)
    const [showDialogBox,setDialogBox] = useState(false)

    const [file, setFile] = useState(null)

    const [data, setData] = useState([]);

    async function fetchData() {
        const d = await fetchRecipeData();

        setData(d);

        console.log(d);

    }

    useEffect(() => {

        fetchData()

    }, [state]);

    const fileChanged = (e) => {
        setFile(e.target.files[0])
    }

    const onSubmit = (data) => {

        uploadRecipe(data.file[0]);

        const restaurantId = localStorage.getItem("id")
        console.log(restaurantId)

        const json = { receipeId: uuid(), recipeName: data.name, restaurantId: restaurantId, fileName: data.file[0].name, price: data.price, restaurantOwner: localStorage.getItem("userEmail") }

        putRecipeData(json)

        setState(state + 1)

    }

    const extract = async (data) => {

        await extractData(data);

    }


    const updateFile = () => {

        uploadRecipe(file);

        updateRecipe(recipeObj.id, file.name)

        setDialogBox(false)
        setState({ "fileUpload": file, "createRecipe": 0 });

    }

    const showDialog = recipe => {
        setDialogBox(true)
        setRecipeObj(recipe)

    }

    const handleClose = () => {
        setDialogBox(false)
        setRecipeObj(null)
    }

    return (
        <div>
            <Form onSubmit={handleSubmit(onSubmit)}>
                <Form.Field>
                    {/* <label>Choose File</label> */}
                    <input placeholder='Enter Recipe Name' type="text" {...register('name', { required: true })} />
                    <input placeholder='Enter Price' type="number" {...register('price', { required: true })} />
                    <input placeholder='Choose File' type="file" {...register('file', { required: true })} />
                </Form.Field>
                <Button type='submit'>Submit</Button>
            </Form>

            <Table singleLine>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Recipe Name</Table.HeaderCell>
                        <Table.HeaderCell>File Name</Table.HeaderCell>
                        <Table.HeaderCell>Price</Table.HeaderCell>
                        <Table.HeaderCell>Extract</Table.HeaderCell>
                        <Table.HeaderCell>Upload</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>

                <Table.Body>
                    {data?.map((row) => {
                        return (
                            <Table.Row>
                                {/* {row.id} */}
                                <Table.Cell>{row.name}</Table.Cell>
                                <Table.Cell>{row.fileName}</Table.Cell>
                                <Table.Cell>{row.price}</Table.Cell>
                                <Table.Cell>
                                    <Button onClick={() => extract(row)}>Extract</Button>
                                </Table.Cell>

                                <Table.Cell>
                                    <Button onClick={() => showDialog(row)}>Upload</Button>
                                    {/* <input type="file" style={{display: 'none'}} id={"recipeImage" + row.id } ref={fileUploadRef} onChange={(e) => uploadImageChanged(e, row.id)}/>
                                    <label htmlFor={"recipeImage" + row.id }><Button onClick={() => upload(row)}>Upload</Button></label> */}
                                </Table.Cell>
                            </Table.Row>
                        )
                    })}
                </Table.Body>
            </Table>
            <Modal show={showDialogBox} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Modal heading</Modal.Title>
                </Modal.Header>
                <Modal.Body><input type="file" onChange={fileChanged}/></Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={() => updateFile()}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>

            {/* <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>File Name</th>
                        <th>Extract</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>Mark</td>
                        <td><Button variant="Primary" onClick={extract}>Extract</Button></td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>Jacob</td>
                        <td><Button variant="Primary" onClick={extract}>Extract</Button></td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>Larry the Bird</td>
                        <td><Button variant="Primary" onClick={extract}>Extract</Button></td>
                    </tr>
                </tbody>
            </Table> */}
        </div>
    );
}

export default DataProcessing;
