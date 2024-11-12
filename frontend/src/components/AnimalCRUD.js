import React, { useState } from 'react';
import './CRUD.css';

function AnimalCRUD() {
    const [columns] = useState(['Index', 'Last Name', 'First Name', 'Age', 'Job', 'Address', 'Actions']);
    const [persons, setPersons] = useState([
        { lname: "ADIASSA", fname: "Ethiel", age: 20, job: "Web Developer", address: "Lome-Togo" },
        { lname: "ADUFU", fname: "Patrick", age: 20, job: "Banker", address: "Senegal-Dakar" },
        { lname: "MOUTON", fname: "John", age: 28, job: "Scientist", address: "New-York/USA" },
        { lname: "SMITH", fname: "Luther", age: 18, job: "Pilot", address: "London/GB" },
        { lname: "WALTER", fname: "Ramses Peter", age: 38, job: "Doctor", address: "Paris/France" },
        { lname: "GEORGES", fname: "Luther", age: 45, job: "Musician", address: "Vienne" },
        { lname: "MICHAEL", fname: "Daven", age: 27, job: "Boxer", address: "Pekin/China" }
    ]);
    const [bin, setBin] = useState([]);
    const [input, setInput] = useState({ lname: '', fname: '', age: '', job: '', address: '' });
    const [editInput, setEditInput] = useState({ lname: '', fname: '', age: '', job: '', address: '' });
    const [isEditing, setIsEditing] = useState(false);

    const addPerson = () => {
        setPersons([...persons, input]);
        setInput({ lname: '', fname: '', age: '', job: '', address: '' });
    };

    const editPerson = (index) => {
        setEditInput(persons[index]);
        setIsEditing(true);
    };

    const updatePerson = () => {
        setPersons(persons.map(person => (person === editInput ? editInput : person)));
        setEditInput({ lname: '', fname: '', age: '', job: '', address: '' });
        setIsEditing(false);
    };

    const archivePerson = (index) => {
        setBin([...bin, persons[index]]);
        setPersons(persons.filter((_, i) => i !== index));
    };

    const restorePerson = (index) => {
        setPersons([...persons, bin[index]]);
        setBin(bin.filter((_, i) => i !== index));
    };

    const depletePerson = (index) => {
        setBin(bin.filter((_, i) => i !== index));
    };

    return (
        <div>
            <div id="app">
                <h4 className="head">Application</h4>
                <div className="container">
                    <table className="table-responsive bordered highlight centered hoverable z-depth-2">
                        <thead>
                            <tr>
                                {columns.map((column, index) => (
                                    <th key={index}>{column}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {persons.map((person, index) => (
                                <tr key={index}>
                                    <td>{index}</td>
                                    <td>{person.lname}</td>
                                    <td>{person.fname}</td>
                                    <td>{person.age} years</td>
                                    <td>{person.job}</td>
                                    <td>{person.address}</td>
                                    <td style={{ width: '18%' }}>
                                        <button onClick={() => editPerson(index)} className="btn waves-effect waves-light yellow darken-2">
                                            <i className="material-icons">edit</i>
                                        </button>
                                        <button onClick={() => archivePerson(index)} className="btn waves-effect waves-light red darken-2">
                                            <i className="material-icons">archive</i>
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            <tr>
                                <td colSpan="2">
                                    <input placeholder="Last Name" value={input.lname} onChange={(e) => setInput({ ...input, lname: e.target.value })} />
                                </td>
                                <td>
                                    <input placeholder="First Name" value={input.fname} onChange={(e) => setInput({ ...input, fname: e.target.value })} />
                                </td>
                                <td>
                                    <input placeholder="Age" value={input.age} onChange={(e) => setInput({ ...input, age: e.target.value })} />
                                </td>
                                <td>
                                    <input placeholder="Job" value={input.job} onChange={(e) => setInput({ ...input, job: e.target.value })} />
                                </td>
                                <td>
                                    <input placeholder="Address" value={input.address} onChange={(e) => setInput({ ...input, address: e.target.value })} />
                                </td>
                                <td>
                                    <button onClick={addPerson} className="btn waves-effect waves-light green darken-2">
                                        <i className="material-icons">add</i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    {isEditing && (
                        <div className="modal">
                            <h4>Edit Person</h4>
                            <input placeholder="Last Name" value={editInput.lname} onChange={(e) => setEditInput({ ...editInput, lname: e.target.value })} />
                            <input placeholder="First Name" value={editInput.fname} onChange={(e) => setEditInput({ ...editInput, fname: e.target.value })} />
                            <input placeholder="Age" value={editInput.age} onChange={(e) => setEditInput({ ...editInput, age: e.target.value })} />
                            <input placeholder="Job" value={editInput.job} onChange={(e) => setEditInput({ ...editInput, job: e.target.value })} />
                            <input placeholder="Address" value={editInput.address} onChange={(e) => setEditInput({ ...editInput, address: e.target.value })} />
                            <button onClick={updatePerson} className="btn">Update</button>
                            <button onClick={() => setIsEditing(false)} className="btn">Cancel</button>
                        </div>
                    )}
                </div>

                <h5>Archived Persons</h5>
                <table className="table-responsive centered bordered striped highlight z-depth-1 hoverable">
                    <thead>
                        <tr>
                            {columns.map((column, index) => (
                                <th key={index}>{column}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {bin.map((person, index) => (
                            <tr key={index}>
                                <td>{index}</td>
                                <td>{person.lname}</td>
                                <td>{person.fname}</td>
                                <td>{person.age} years</td>
                                <td>{person.job}</td>
                                <td>{person.address}</td>
                                <td>
                                    <button onClick={() => restorePerson(index)} className="btn waves-effect waves-light blue darken-2">
                                        <i className="material-icons">restore</i>
                                    </button>
                                    <button onClick={() => depletePerson(index)} className="btn waves-effect waves-light red darken-2">
                                        <i className="material-icons">delete</i>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AnimalCRUD;
