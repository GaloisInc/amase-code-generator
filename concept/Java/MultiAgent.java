package amase.examples;
import afrl.cmasi.SessionStatus;
import afrl.cmasi.Play;
import java.util.HashMap;
import avtas.app.UserExceptions;
import avtas.amase.AmasePlugin;
import avtas.amase.scenario.ScenarioEvent;
import avtas.amase.scenario.ScenarioState;
import avtas.amase.util.CmasiNavUtils;
import avtas.amase.util.CmasiUtils;
import avtas.app.AppEventManager;
import avtas.util.NavUtils;
import java.awt.Component;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.TreeMap;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;


public class MultiAgent extends AmasePlugin {

    JPanel panel;
    JButton uav1Loiter;
    JButton uav1SearchTrackUAV2inA;
    JButton uav1SearchTrackUAV2inB;
    JButton uav2Loiter;
    SessionStatus lastStatus = null;

    public MultiAgent() {
        setPluginName("Multi-Agent");
        setupGui();
    }

    @Override
    public void eventOccurred(Object event) {
        if (event instanceof ScenarioEvent) {
            initScenario((ScenarioEvent) event);
        }
        else if (event instanceof SessionStatus) {
            lastStatus = (SessionStatus) event;
        }
    }

    protected void initScenario(ScenarioEvent scenarioEvent) {
        System.out.println("New Scenario loaded.");
            uav1Loiter.setEnabled(true);
            uav1SearchTrackUAV2inA.setEnabled(true);
            uav1SearchTrackUAV2inB.setEnabled(true);
            uav2Loiter.setEnabled(true);
    }

    @Override
    public Component getGui() {
        return panel;
    }

    protected void setupGui() {
        panel = new JPanel();
        panel.setLayout(new FlowLayout(FlowLayout.CENTER));
        panel.setBorder(new EmptyBorder(5, 5, 5, 5));
        uav1Loiter = new JButton("UAV1 Loiter");
        uav1SearchTrackUAV2inA = new JButton("UAV1 ST UAV2 A");
        uav1SearchTrackUAV2inB = new JButton("UAV1 ST UAV2 B");
        uav2Loiter = new JButton("UAV2 Loiter");
        panel.add(uav1Loiter);
        panel.add(uav1SearchTrackUAV2inA);
        panel.add(uav1SearchTrackUAV2inB);
        panel.add(uav2Loiter);

        // set the button to be disabled until a task is loaded in the scenario
        uav1Loiter.setEnabled(false);
        uav1SearchTrackUAV2inA.setEnabled(false);
        uav1SearchTrackUAV2inB.setEnabled(false);
        uav2Loiter.setEnabled(false);

        uav1Loiter.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify11();
            }
        });
        uav1SearchTrackUAV2inA.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify12();
            }
        });
        uav1SearchTrackUAV2inB.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify21();
            }
        });
        uav2Loiter.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify22();
            }
        });
    }
    private void notify11() {
        String str = new String(" ");
        // get a list of the current state of all aircraft in the scenario

        str = new String("This is play: ");

        str = str + "UAV1 Loiter.";
        
        System.out.println(str);

        sendPlay(1,1);
    }

    private void notify12() {
        String str = new String(" ");
        // get a list of the current state of all aircraft in the scenario

        str = new String("This is play: ");

        str = str + "UAV1 Search & Track UAV2 in A";

        System.out.println(str);
        sendPlay(2,1);

    }    

    private void notify21() {
        String str = new String(" ");
        // get a list of the current state of all aircraft in the scenario

        str = new String("This is play: ");

        str = str + "UAV1 Search & Track UAV2 in B";

        System.out.println(str);
        sendPlay(3,1);

    }    

    private void notify22() {
        String str = new String(" ");
        // get a list of the current state of all aircraft in the scenario

        str = new String("This is play: ");

        str = str + "UAV2 Loiter.";

        System.out.println(str);
        sendPlay(1,2);

    }    

    void sendPlay(int a, int b) {

        // create a new CMASI zone.  In this case, a KeepOutZone.
        Play play = new Play();
        play.setPlayID(a);
        play.setUAVID(b);
        play.setTime(lastStatus.getScenarioTime());

        // tells the plugin to fire the task to the rest of the application
        fireEvent(play);
    }
    
    

}