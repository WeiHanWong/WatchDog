package com.example.watchdog;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.MenuItem;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationBarView;

public class MainMenu extends AppCompatActivity {

    BottomNavigationView bottomNavigationView;

    DashboardFragment dashboardFragment = new DashboardFragment();
    LocationsFragment locationsFragment = new LocationsFragment();
    AboutFragment aboutFragment = new AboutFragment();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_menu);

        bottomNavigationView = findViewById(R.id.bottomNav);

        getSupportFragmentManager().beginTransaction().replace(R.id.frame,
                dashboardFragment).commit();

        bottomNavigationView.setOnItemSelectedListener(new NavigationBarView
                .OnItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId()) {
                    case 1000015:
                        getSupportFragmentManager().beginTransaction().replace(R.id.frame,
                                dashboardFragment).commit();
                        return true;

                    case 1000011:
                        getSupportFragmentManager().beginTransaction().replace(R.id.frame,
                                locationsFragment).commit();
                        return true;

                    case 1000012:
                        getSupportFragmentManager().beginTransaction().replace(R.id.frame,
                                aboutFragment).commit();
                        return true;
                }

                return false;
            }
        });

    }
}
