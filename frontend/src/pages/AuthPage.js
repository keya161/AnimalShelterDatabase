import React, { useState } from 'react';

const LoginRegisterForm = () => {
    const [activeTab, setActiveTab] = useState('signup');
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        loginEmail: '',
        loginPassword: ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e, type) => {
        e.preventDefault();
        // Handle form submission based on type (login/register)
        console.log(`${type} submission:`, formData);
    };

    const InputField = ({ label, name, type = 'text', isLogin = false }) => {
        const [isFocused, setIsFocused] = useState(false);
        const fieldName = isLogin ? `login${name.charAt(0).toUpperCase() + name.slice(1)}` : name;
        const value = formData[fieldName];

        return (
            <div className="field-wrap">
                <label className={`${value || isFocused ? 'active' : ''} ${isFocused ? 'highlight' : ''}`}>
                    {label}<span className="req">*</span>
                </label>
                <input
                    type={type}
                    required
                    name={fieldName}
                    value={value}
                    onChange={handleInputChange}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    autoComplete="off"
                />
            </div>
        );
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-[#c1bdba] font-['Titillium_Web']">
            <div className="form">
                <ul className="tab-group">
                    <li className={`tab ${activeTab === 'signup' ? 'active' : ''}`}>
                        <a onClick={() => setActiveTab('signup')}>Register</a>
                    </li>
                    <li className={`tab ${activeTab === 'login' ? 'active' : ''}`}>
                        <a onClick={() => setActiveTab('login')}>Log In</a>
                    </li>
                </ul>

                <div className="tab-content">
                    {activeTab === 'signup' && (
                        <div id="signup">
                            <h1>Register for Free!</h1>
                            <form onSubmit={(e) => handleSubmit(e, 'register')}>
                                <div className="top-row">
                                    <div>
                                        <InputField label="First Name" name="firstName" />
                                    </div>
                                    <div>
                                        <InputField label="Last Name" name="lastName" />
                                    </div>
                                </div>
                                <InputField label="Email" name="email" type="email" />
                                <InputField
                                    label="Password"
                                    name="password"
                                    type="password"
                                />
                                <button type="submit" className="button button-block">
                                    Register
                                </button>
                            </form>
                        </div>
                    )}

                    {activeTab === 'login' && (
                        <div id="login">
                            <h1>Welcome!</h1>
                            <form onSubmit={(e) => handleSubmit(e, 'login')}>
                                <InputField
                                    label="Email"
                                    name="email"
                                    type="email"
                                    isLogin
                                />
                                <InputField
                                    label="Password"
                                    name="password"
                                    type="password"
                                    isLogin
                                />
                                <div className="forgot">
                                    <a href="#">Forgot Password?</a>
                                </div>
                                <div className="forgot">
                                    <a href="#">Forgot Email?</a>
                                </div>
                                <button type="submit" className="button button-block">
                                    Log In
                                </button>
                            </form>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default LoginRegisterForm;