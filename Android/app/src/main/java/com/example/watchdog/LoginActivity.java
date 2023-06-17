package com.example.watchdog;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextUtils;
import android.text.method.LinkMovementMethod;
import android.text.style.ClickableSpan;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class LoginActivity extends AppCompatActivity {

    EditText emailTxt;
    EditText pwdTxt;
    Button login_btn;
    TextView forgotPwd;
    TextView toRegTxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        emailTxt = findViewById(R.id.emailText);
        pwdTxt = findViewById(R.id.pwdText);
        login_btn = findViewById(R.id.registerBtn);
        forgotPwd = findViewById(R.id.forgotPwd);
        toRegTxt = findViewById(R.id.toSignTxt);

        String fp = "Forgot Password?";
        String toReg = "New to WatchDog? Register Here!";
        SpannableString ss1 = new SpannableString(fp);
        SpannableString ss2 = new SpannableString(toReg);

        ClickableSpan cs1 = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                // TODO: Implement forgot pwd function
            }
        };

        ClickableSpan cs2 = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                Intent intent = new Intent(LoginActivity.this, RegisterActivity.class);
                startActivity(intent);
                finish();
            }
        };

        ss1.setSpan(cs1, 0, fp.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        ss2.setSpan(cs2, 17, toReg.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);

        forgotPwd.setText(ss1);
        toRegTxt.setText(ss2);
        forgotPwd.setMovementMethod(LinkMovementMethod.getInstance());
        toRegTxt.setMovementMethod(LinkMovementMethod.getInstance());

        login_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                chkLoginCredentials();
            }
        });

    }

    boolean isEmpty(EditText text) {
        CharSequence str = text.getText().toString();
        return TextUtils.isEmpty(str);
    }

    boolean isEmail(EditText text) {
        CharSequence email = text.getText().toString();
        return (!TextUtils.isEmpty(email) && !Patterns.EMAIL_ADDRESS.matcher(email).matches());
    }

    private void chkLoginCredentials() {
        if (isEmpty(emailTxt) || isEmpty(pwdTxt)) {
            Toast.makeText(this, "Please fill in the fields!",
                    Toast.LENGTH_SHORT).show();
        } else if (isEmail(emailTxt)) {
            Toast.makeText(this, "Invalid email address", Toast.LENGTH_SHORT).show();
        } else {
            login();
        }
    }

    private void login() {

    }

}