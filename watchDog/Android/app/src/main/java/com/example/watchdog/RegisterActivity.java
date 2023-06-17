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

public class RegisterActivity extends AppCompatActivity {

    TextView toSignTxt;
    EditText nameTxt;
    EditText emailTxt;
    EditText pwdTxt;
    EditText confirmPwdTxt;
    Button registerBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        toSignTxt = findViewById(R.id.toSignTxt);
        nameTxt = findViewById(R.id.nameText);
        emailTxt = findViewById(R.id.emailText);
        pwdTxt = findViewById(R.id.pwdText);
        confirmPwdTxt = findViewById(R.id.cPwdText);
        registerBtn = findViewById(R.id.registerBtn);

        String toSignIn = "Already have an account? Sign in!";
        SpannableString ss = new SpannableString(toSignIn);

        ClickableSpan cs = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
                startActivity(intent);
                finish();
            }
        };

        ss.setSpan(cs, 25, toSignIn.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        toSignTxt.setText(ss);
        toSignTxt.setMovementMethod(LinkMovementMethod.getInstance());

        registerBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                chkRegCredentials();
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

    private void chkRegCredentials() {
        if (isEmpty(nameTxt) || isEmpty(emailTxt) || isEmpty(pwdTxt) || isEmpty(confirmPwdTxt)) {
            Toast.makeText(this, "Please fill in the fields!",
                    Toast.LENGTH_SHORT).show();
        } else if (isEmail(emailTxt)) {
            Toast.makeText(this, "Invalid email address", Toast.LENGTH_SHORT).show();
        } else if (!pwdTxt.getText().toString().equals(confirmPwdTxt.getText().toString())) {
            Toast.makeText(this, "Password does not match", Toast.LENGTH_SHORT).show();
        } else {
            register();
        }

    }

    private void register() {

    }

}