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


public class PlayGUI extends AmasePlugin {

    JPanel panel;
    SessionStatus lastStatus = null;

    JButton uav1Loiter;
    JButton uav1SearchTrackUAV2inA;
    JButton uav1SearchTrackUAV2inB;
    JButton uav2Loiter;

    public PlayGUI() {
        setPluginName("Play-GUI");
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
	    panel.add(uav1Loiter);
	    uav1Loiter.setEnabled(false);
        uav1Loiter.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify11();
            }
        });

        uav1SearchTrackUAV2inA = new JButton("UAV1 ST UAV2 A");
        panel.add(uav1SearchTrackUAV2inA);
        uav1SearchTrackUAV2inA.setEnabled(false);
        uav1SearchTrackUAV2inA.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify21();
            }
        });

        uav1SearchTrackUAV2inB = new JButton("UAV1 ST UAV2 B");
        uav1SearchTrackUAV2inB.setEnabled(false);
        panel.add(uav1SearchTrackUAV2inB);
        uav1SearchTrackUAV2inB.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify31();
            }
        });

        uav2Loiter = new JButton("UAV2 Loiter");
        panel.add(uav2Loiter);
        uav2Loiter.setEnabled(false);
        uav2Loiter.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify12();
            }
        });

    }
    private void notify11() {
        sendPlay(1,1);
    }

    private void notify21() {
        sendPlay(2,1);
    }    

    private void notify31() {
        sendPlay(3,1);
    }    

    private void notify12() {
        sendPlay(1,2);
    }    

    void sendPlay(int a, int b) {

        Play play = new Play();
        play.setPlayID(a);
        play.setUAVID(b);
        play.setTime(lastStatus.getScenarioTime());

        fireEvent(play);
    }
}
