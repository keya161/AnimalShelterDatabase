// src/components/LoginForm.js

import React, { useState } from 'react';
import axios from 'axios';

function LoginForm() {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/api/auth/login', formData);
            alert("Login successful");
        } catch (error) {
            console.error("Login failed", error);
        }
    };

    return (
        <div>
            <h1>Welcome!</h1>
            <form onSubmit={handleSubmit}>
                <div className="field-wrap">
                    <label>Email<span className="req"></span></label>
                    <input type="email" name="email" required value={formData.email} onChange={handleChange} />
                </div>
                <div className="field-wrap">
                    <label>Password<span className="req"></span></label>
                    <input type="password" name="password" required value={formData.password} onChange={handleChange} />
                </div>
                <button type="submit" className="button button-block">Log In</button>
            </form>
        </div>
    );
}

export default LoginForm;
