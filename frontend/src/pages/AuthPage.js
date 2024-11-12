import './AuthPage.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import $ from 'jquery'; // Import jQuery if you need to use it

function AuthPage() {
    useEffect(() => {
        $('.form').find('input, textarea').on('keyup blur focus', function (e) {
            var $this = $(this),
                label = $this.prev('label');

            if (e.type === 'keyup') {
                if ($this.val() === '') {
                    label.removeClass('active highlight');
                } else {
                    label.addClass('active highlight');
                }
            } else if (e.type === 'blur') {
                if ($this.val() === '') {
                    label.removeClass('active highlight');
                } else {
                    label.removeClass('highlight');
                }
            } else if (e.type === 'focus') {
                if ($this.val() === '') {
                    label.removeClass('highlight');
                } else if ($this.val() !== '') {
                    label.addClass('highlight');
                }
            }
        });

        $('.tab a').on('click', function (e) {
            e.preventDefault();
            $(this).parent().addClass('active');
            $(this).parent().siblings().removeClass('active');
            let target = $(this).attr('href');
            $('.tab-content > div').not(target).hide();
            $(target).fadeIn(600);
        });
    }, []);

    return (
        <div className="form">
            <ul className="tab-group">
                <li className="tab active"><a href="#signup">Register</a></li>
                <li className="tab"><a href="#login">Log In</a></li>
            </ul>

            <div className="tab-content">
                <div id="signup">
                    <h1>Register</h1>
                    <form action="/" method="post">
                        <div className="top-row">
                            <div className="field-wrap">
                                <label>
                                    First Name<span className="req">*</span>
                                </label>
                                <input type="text" required autoComplete="off" />
                            </div>
                            <div className="field-wrap">
                                <label>
                                    Last Name<span className="req">*</span>
                                </label>
                                <input type="text" required autoComplete="off" />
                            </div>
                        </div>
                        <div className="field-wrap">
                            <label>
                                Username<span className="req">*</span>
                            </label>
                            <input type="text" required autoComplete="off" />
                        </div>
                        <div className="field-wrap">
                            <label>
                                Password<span className="req">*Minimum 6 characters!</span>
                            </label>
                            <input type="password" required autoComplete="off" />
                        </div>
                        <button type="submit" className="button button-block">Register</button>
                    </form>
                </div>

                <div id="login">
                    <h1>Welcome!</h1>
                    <form action="/" method="post">
                        <div className="field-wrap">
                            <label>
                                Email<span className="req"></span>
                            </label>
                            <input type="email" required autoComplete="off" />
                        </div>
                        <div className="field-wrap">
                            <label>
                                Password<span className="req"></span>
                            </label>
                            <input type="password" required autoComplete="off" />
                        </div>
                        <button type="submit" className="button button-block">Log In</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default AuthPage;
