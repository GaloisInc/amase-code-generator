
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
    JButton P_1_ST_0_1;
    JButton P_1_Loiter_0_0;
    JButton P_1_ST_0_0;
    JButton P_0_Loiter_0_0;
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
        P_1_ST_0_1.setEnabled(true);
        P_1_Loiter_0_0.setEnabled(true);
        P_1_ST_0_0.setEnabled(true);
        P_0_Loiter_0_0.setEnabled(true);
    }
    @Override
    public Component getGui() {
        return panel;
    }
    protected void setupGui() {
        panel = new JPanel();
        panel.setLayout(new FlowLayout(FlowLayout.CENTER));
        panel.setBorder(new EmptyBorder(5, 5, 5, 5));
        P_1_ST_0_1 = new JButton("P_1_ST_0_1");
        panel.add(P_1_ST_0_1);
        P_1_ST_0_1.setEnabled(false);
        P_1_ST_0_1.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify12();
            }
        });
        P_1_Loiter_0_0 = new JButton("P_1_Loiter_0_0");
        panel.add(P_1_Loiter_0_0);
        P_1_Loiter_0_0.setEnabled(false);
        P_1_Loiter_0_0.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify22();
            }
        });
        P_1_ST_0_0 = new JButton("P_1_ST_0_0");
        panel.add(P_1_ST_0_0);
        P_1_ST_0_0.setEnabled(false);
        P_1_ST_0_0.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify32();
            }
        });
        P_0_Loiter_0_0 = new JButton("P_0_Loiter_0_0");
        panel.add(P_0_Loiter_0_0);
        P_0_Loiter_0_0.setEnabled(false);
        P_0_Loiter_0_0.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                notify11();
            }
        });
    }
    private void notify12() {
        sendPlay(1,2);
    }
    private void notify22() {
        sendPlay(2,2);
    }
    private void notify32() {
        sendPlay(3,2);
    }
    private void notify11() {
        sendPlay(1,1);
    }
    void sendPlay(int a, int b) {
        Play play = new Play();
        play.setPlayID(a);
        play.setUAVID(b);
        play.setTime(lastStatus.getScenarioTime());
        fireEvent(play);
    }
}