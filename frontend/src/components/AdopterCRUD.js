import React, { useState, useEffect } from 'react';
import './CRUD2.css'

const UserManagement = () => {
    const [users, setUsers] = useState([
        { id: 1, name: 'Bob', address: 'Manila', age: 27 },
        { id: 2, name: 'Harry', address: 'Baguio', age: 32 },
    ]);
    const [newUser, setNewUser] = useState({ name: '', address: '', age: '' });
    const [userToEdit, setUserToEdit] = useState(null);

    useEffect(() => {
        // This will run once when the component mounts.
        // You can add any necessary initialization logic here.
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewUser({ ...newUser, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const { name, address, age } = newUser;

        if (name && address && age) {
            const newId = users[users.length - 1].id + 1;
            const user = { ...newUser, id: newId };
            setUsers([...users, user]);
            setNewUser({ name: '', address: '', age: '' }); // Clear the input fields
        } else {
            alert('All fields must have a valid value.');
        }
    };

    const handleEdit = (id) => {
        const user = users.find(user => user.id === id);
        setUserToEdit(user);
    };

    const handleDelete = (id) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            const updatedUsers = users.filter(user => user.id !== id);
            setUsers(updatedUsers);
            alert('User deleted successfully!');
        }
    };

    const handleUpdate = (e) => {
        e.preventDefault();
        if (userToEdit) {
            const updatedUsers = users.map(user =>
                user.id === userToEdit.id ? userToEdit : user
            );
            setUsers(updatedUsers);
            setUserToEdit(null); // Close the modal
            alert('User updated successfully!');
        }
    };

    return (
        <div className="container">
            <div className="row">
                <div className="col-md-4">
                    <h3>ADD USER</h3>
                    <form id="addUser" onSubmit={handleSubmit}>
                        <div className="form-group">
                            <input
                                className="form-control"
                                type="text"
                                name="name"
                                value={newUser.name}
                                onChange={handleInputChange}
                                placeholder="Name"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <input
                                className="form-control"
                                type="text"
                                name="address"
                                value={newUser.address}
                                onChange={handleInputChange}
                                placeholder="Address"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <input
                                className="form-control"
                                type="number"
                                name="age"
                                min="10"
                                max="100"
                                value={newUser.age}
                                onChange={handleInputChange}
                                placeholder="Age"
                                required
                            />
                        </div>
                        <button className="btn btn-primary form-control" type="submit">
                            SUBMIT
                        </button>
                    </form>
                </div>

                <div className="col-md-8">
                    <h3>USERS</h3>
                    <table id="userTable" className="table table-striped">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Address</th>
                                <th>Age</th>
                                <th colSpan="2">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map((user) => (
                                <tr key={user.id} id={`user-${user.id}`}>
                                    <td>{user.name}</td>
                                    <td>{user.address}</td>
                                    <td>{user.age}</td>
                                    <td align="center">
                                        <button
                                            className="btn btn-success form-control"
                                            onClick={() => handleEdit(user.id)}
                                            data-toggle="modal"
                                            data-target="#myModal"
                                        >
                                            EDIT
                                        </button>
                                    </td>
                                    <td align="center">
                                        <button
                                            className="btn btn-danger form-control"
                                            onClick={() => handleDelete(user.id)}
                                        >
                                            DELETE
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Modal for editing user */}
            {userToEdit && (
                <div className="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                                <h4 className="modal-title" id="myModalLabel">Update User</h4>
                            </div>
                            <div className="modal-body">
                                <form id="updateUser" onSubmit={handleUpdate}>
                                    <div className="form-group">
                                        <label>Name</label>
                                        <input
                                            className="form-control"
                                            type="text"
                                            name="name"
                                            value={userToEdit.name}
                                            onChange={(e) => setUserToEdit({ ...userToEdit, name: e.target.value })}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label>Address</label>
                                        <input
                                            className="form-control"
                                            type="text"
                                            name="address"
                                            value={userToEdit.address}
                                            onChange={(e) => setUserToEdit({ ...userToEdit, address: e.target.value })}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label>Age</label>
                                        <input
                                            className="form-control"
                                            type="number"
                                            name="age"
                                            min="10"
                                            max="100"
                                            value={userToEdit.age}
                                            onChange={(e) => setUserToEdit({ ...userToEdit, age: e.target.value })}
                                        />
                                    </div>
                                    <button type="submit" className="btn btn-primary">
                                        Save changes
                                    </button>
                                    <button type="button" className="btn btn-default" data-dismiss="modal">
                                        Close
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UserManagement;
