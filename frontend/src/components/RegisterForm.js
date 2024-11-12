// src/components/RegisterForm.js

import React, { useState } from 'react';
import axios from 'axios';

function RegisterForm() {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/api/auth/register', formData);
            alert("Registration successful");
        } catch (error) {
            console.error("Registration failed", error);
        }
    };

    return (
        <div>
            <h1>Register for Free!</h1>
            <form onSubmit={handleSubmit}>
                <div className="top-row">
                    <div className="field-wrap">
                        <label>First Name<span className="req">*</span></label>
                        <input type="text" name="firstName" required value={formData.firstName} onChange={handleChange} />
                    </div>
                    <div className="field-wrap">
                        <label>Last Name<span className="req">*</span></label>
                        <input type="text" name="lastName" required value={formData.lastName} onChange={handleChange} />
                    </div>
                </div>
                <div className="field-wrap">
                    <label>Email<span className="req">*</span></label>
                    <input type="email" name="email" required value={formData.email} onChange={handleChange} />
                </div>
                <div className="field-wrap">
                    <label>Password<span className="req">*</span></label>
                    <input type="password" name="password" required value={formData.password} onChange={handleChange} />
                </div>
                <button type="submit" className="button button-block">Register</button>
            </form>
        </div>
    );
}

export default RegisterForm;
