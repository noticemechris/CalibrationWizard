package org.overlake.mat803.calibrationwizard;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import static android.view.Gravity.CENTER_HORIZONTAL;
import static android.view.Gravity.CENTER_VERTICAL;

public class StepActivity extends AppCompatActivity {


    private Button mNextButton;
    private Button mPrevButton;
    private TextView mStepTextView;
    private int[] mStepList;
    private int mCurrentIndex;
    public static final String TAG = "StepActivity";
    public static final String KEY_INDEX = "currentIndex";

    public StepActivity(){
        //I will talk to david about how to cycle through the steps,
        //and alternatives to just using a question bank. These are mostly
        //placeholders for now. Will als make UI prettier when I feel like it.
        mStepList = new int[]{
            R.string.step_one,
            R.string.step_two,
            R.string.step_three,
            R.string.step_four,
            R.string.step_five_nine,
            R.string.step_ten,
        };
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (savedInstanceState != null) {
            mCurrentIndex = savedInstanceState.getInt(KEY_INDEX, 0);
        }

        setContentView(R.layout.activity_quiz);
        Log.d(TAG, "onCreate() called");
        mStepTextView = findViewById(R.id.step_view);
        mNextButton = findViewById(R.id.next_button);
        mPrevButton = findViewById(R.id.prev_button);
        updateStep();

        mNextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mCurrentIndex += 1;
                if (mCurrentIndex == mStepList.length) {
                    mCurrentIndex = mStepList.length - 1;
                    updateStep();
                }

                updateStep();
            }
        });

        mPrevButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                    mCurrentIndex -= 1;
                    if(mCurrentIndex == -1) {
                        mCurrentIndex = 0;
                    }

                    updateStep();
            }
        });
    }

    private void updateStep() {
        //talk to david about how to efficiently instert strings, I tried but it was having emotional issues.
            mStepTextView.setText(mStepList[mCurrentIndex]);
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.d(TAG, "onStart() called");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG, "onResume() called");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.d(TAG, "onPause() called");
    }

    @Override
    protected void onStop() {
        super.onStop();
        Log.d(TAG, "onStop() called");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy() called");
    }

    @Override
    protected void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        Log.d(TAG, "onSaveInstanceState() called()");
        outState.putInt(KEY_INDEX, mCurrentIndex);
    }
}