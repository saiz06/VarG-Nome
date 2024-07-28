package GraphCreator;
import org.jfree.chart.JFreeChart;

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class GraphGUI extends JFrame implements ActionListener {
    JPanel p = new JPanel();
    CardLayout layout = new CardLayout();
    JTextField f1 = new JTextField(), f2 = new JTextField(), f3 = new JTextField(), f4 = new JTextField(),
            f5 = new JTextField(), f6 = new JTextField(), f7 = new JTextField(), f8 = new JTextField(),
            f9 = new JTextField(), f10 = new JTextField();
    JTextField[] fields = {f1, f2, f3, f4, f5, f6, f7, f8, f9, f10};
    JTextField name = new JTextField(), xField = new JTextField(), yField = new JTextField();
    File inFile;
    String[][][] manualStore = new String[5][5][2];
    boolean[] visited = {false, false, false, false, false};
    String mode = "";
    String nameVal = "", xVal = "", yVal = "";
    String method = "";

    int selectPrev;
    int manualPage = 0;

    public GraphGUI() {
        setTitle("Graph GUI");
        setSize(400, 400);
        p.setLayout(layout);
        p.add(graphSelect(), "START");
        p.add(nameAndAxes(), "INFO");
        p.add(choosePage(), "CHOOSE");
        p.add(fromCSVPage(), "CSV");
        p.add(manualInput(), "MANUAL");

        this.setContentPane(p);
        layout.show(p, "START");
    }

    // Page 0
    public JPanel choosePage() {
        JPanel choose = new JPanel();
        JLabel l1 = new JLabel("Would you like to import a CSV file or input your own data?");
        JLabel l2 = new JLabel("(You may input up to 25 rows manually.)");
        l1.setBounds(25, 25, 400, 30);
        l2.setBounds(25, 50, 400, 30);
        JButton b1 = new JButton("Import file");
        JButton b2 = new JButton("Input manually");
        b1.setBounds(25,100,150,20);
        b2.setBounds(200, 100, 150, 20);
        JButton back = new JButton("Back");
        back.setBounds(112, 200, 150, 20);
        back.addActionListener(this);
        back.setActionCommand("BACK-SELECT");
        b1.addActionListener(this);
        b2.addActionListener(this);
        b1.setActionCommand("CSV");
        b2.setActionCommand("MANUAL");
        choose.add(l1);
        choose.add(l2);
        choose.add(b1);
        choose.add(b2);
        choose.add(back);
        choose.setLayout(null);
        return choose;
    }

    public JPanel fromCSVPage() {
        JPanel csv = new JPanel();
        JLabel l1 = new JLabel("Please select the CSV file to import.");
        l1.setBounds(25, 25, 400, 30);
        JButton b1 = new JButton("Choose file...");
        b1.setBounds(25,75,150,20);
        b1.addActionListener(this);
        b1.setActionCommand("LOAD");
        JButton back = new JButton("Back");
        back.setBounds(25, 225, 150, 20);
        back.addActionListener(this);
        back.setActionCommand("BACK-CSV");
        csv.add(b1);
        csv.add(l1);
        csv.add(back);
        csv.setLayout(null);
        return csv;
    }

    public JPanel csvLoaded(String filename) {
        selectPrev = 0;
        JPanel csv = fromCSVPage();
        JButton next = new JButton("Next");
        next.setBounds(25, 175, 150, 20);
        next.addActionListener(this);
        next.setActionCommand("DONE");
        JLabel loaded = new JLabel();
        loaded.setText("Loaded file " + filename);
        loaded.setBounds(25, 125, 400, 30);
        csv.add(loaded);
        csv.add(next);
        csv.setLayout(null);
        return csv;
    }

    public JPanel nameAndAxes() {
        JPanel info = new JPanel();
        JLabel instr = new JLabel("Please input the name of your graph and its x & y axes.");
        instr.setBounds(25, 25, 400, 30);
        JLabel nameLabel = new JLabel("Name:");
        nameLabel.setBounds(150, 75, 100, 20);
        name.setBounds(125, 100, 150, 30);
        JLabel xLabel = new JLabel("X Axis Label:");
        xLabel.setBounds(150, 150, 150, 20);
        xField.setBounds(125, 175, 150, 30);
        JLabel yLabel = new JLabel("Y Axis Label:");
        yLabel.setBounds(150, 225, 150, 20);
        yField.setBounds(125, 250, 150, 30);
        JButton next = new JButton("Next");
        next.setBounds(250, 300, 100, 30);
        next.addActionListener(this);
        next.setActionCommand("MANUAL");
        JButton back = new JButton("Back");
        back.setBounds(50, 300, 100, 30);
        back.addActionListener(this);
        back.setActionCommand("BACK-INFO");
        info.add(instr); info.add(nameLabel); info.add(name);
        info.add(xLabel); info.add(xField); info.add(yLabel); info.add(yField); info.add(next); info.add(back);
        info.setLayout(null);
        return info;
    }

    public JPanel manualInput() {
        selectPrev = 1;
        JPanel manual = new JPanel();
        JLabel inLabel = new JLabel("Please input your data, then click Next to input more ");
        JLabel inLabel2 = new JLabel("data or Done to finish input.");
        inLabel.setBounds(25, 15, 350, 30);
        inLabel2.setBounds(25, 30, 350, 30);
        JLabel item = new JLabel("Item");
        JLabel value = new JLabel("Value");
        item.setBounds(80, 60, 150, 30);
        value.setBounds(275, 60, 150, 30);
        f1.setBounds(25, 95, 150, 30);
        f2.setBounds(25, 130, 150, 30);
        f3.setBounds(25, 165, 150, 30);
        f4.setBounds(25, 200, 150, 30);
        f5.setBounds(25, 235, 150, 30);
        f6.setBounds(225, 95, 150, 30);
        f7.setBounds(225, 130, 150, 30);
        f8.setBounds(225, 165, 150, 30);
        f9.setBounds(225, 200, 150, 30);
        f10.setBounds(225, 235, 150, 30);
        JButton done = new JButton("Done");
        done.addActionListener(this);
        done.setActionCommand("DONE");
        done.setBounds(150, 305, 100, 30);
        JButton next = new JButton("Next");
        next.addActionListener(this);
        next.setActionCommand("NEXT");
        next.setBounds(250, 270, 100, 30);
        JButton back = new JButton("Back");
        back.setBounds(50, 270, 100, 30);
        back.addActionListener(this);
        back.setActionCommand("BACK-MANUAL");
        manual.add(inLabel); manual.add(inLabel2); manual.add(item); manual.add(value);
        for(JTextField field : fields) {
            manual.add(field);
        }
        manual.add(next); manual.add(done); manual.add(back);
        manual.setLayout(null);
        return manual;
    }

    public void dataStore() {
        for(int i = 0; i <= 4; i++) {
            String[] pair = new String[2];
            if(fields[i].getText() != null) {
                manualStore[manualPage][i][0] = (fields[i].getText());
            }
            else {
                manualStore[manualPage][i][0] = "";
            }
            if(fields[i+5].getText() != null && fields[i+5].getText().matches("-?\\d+(\\.\\d+)?")) {
                manualStore[manualPage][i][1] = fields[i+5].getText();
            }
            else {
                manualStore[manualPage][i][1] = "";
            }
        }
    }

    public JPanel graphSelect() {
        JPanel select = new JPanel();
        JLabel choose = new JLabel("Please choose your graph type:");
        choose.setBounds(25, 25, 300, 30);
        JButton pie = new JButton("Pie");
        pie.setBounds(150, 75, 100, 30);
        pie.addActionListener(this);
        pie.setActionCommand("PIE");
        JButton bar = new JButton("Bar");
        bar.setBounds(150, 125, 100, 30);
        bar.addActionListener(this);
        bar.setActionCommand("BAR");
        //Line graph functionality is currently unavailable
//        JButton line = new JButton("Line");
//        line.setBounds(150, 175, 100, 30);
//        line.addActionListener(this);
//        line.setActionCommand("LINE");
        select.add(choose); select.add(pie); select.add(bar);
        select.setLayout(null);
        return select;
    }

    public void actionPerformed(ActionEvent e) {
        switch (e.getActionCommand()) {
            case "INFO":
                nameVal = name.getText();
                xVal = xField.getText();
                yVal = yField.getText();
                layout.show(p, "CHOOSE");
                break;
            case "CSV":
                layout.show(p, "CSV");
                method = "CSV";
                break;
            case "MANUAL":

                layout.show(p, "MANUAL");
                method = "MANUAL";
                manualPage = 0;
                break;
            case "LOAD":
                JFileChooser fc = new JFileChooser();
                fc.setCurrentDirectory(new File("C:\\Users\\criec\\IdeaProjects\\GraphCreator\\res"));
                fc.setFileFilter(new FileNameExtensionFilter("Comma-Separated Values (CSV)", "CSV"));
                int success = fc.showOpenDialog(this);
                if (success == JFileChooser.APPROVE_OPTION) {
                    inFile = fc.getSelectedFile();
                    String filename = inFile.getName();
                    JPanel csvLoad = csvLoaded(filename);
                    p.add(csvLoad, "LOAD");
                    layout.show(p, "LOAD");
                }
                break;
            case "NEXT":
                visited[manualPage] = true;
                dataStore();
                if (manualPage == 4) {
                    Map<String, Double> dataMap = new HashMap<>();
                    if(method.equals("CSV")) {
                        dataMap = GraphMaps.pieBarData(inFile);
                    }
                    else if(method.equals("MANUAL")) {
                        dataMap = GraphMaps.makeMap(manualStore);
                    }
                    JPanel graph = GraphPanels.createGraph(inFile, dataMap, mode, nameVal, xVal, yVal);
                    p.add(graph, "GRAPH");
                    layout.show(p, "GRAPH");
                } else {
                    manualPage++;
                    layout.show(p, "MANUAL");
                    if (!visited[manualPage]) {
                        for (JTextField field : fields) {
                            field.setText("");
                        }
                    } else {
                        for (int i = 0; i <= 9; i++) {
                            if (i <= 4) {
                                fields[i].setText((String) manualStore[manualPage][i][0]);
                            } else {
                                fields[i].setText((String) manualStore[manualPage][i - 5][1]);
                            }
                        }
                    }
                }
                break;
            case "DONE":
                dataStore();
                Map<String, Double> dataMap = new HashMap<>();
                if(method.equals("CSV")) {
                    dataMap = GraphMaps.pieBarData(inFile);
                }
                else if(method.equals("MANUAL")) {
                    dataMap = GraphMaps.makeMap(manualStore);
                }
                JPanel graph = GraphPanels.createGraph(inFile, dataMap, mode, nameVal, xVal, yVal);
                p.add(graph, "GRAPH");
                layout.show(p, "GRAPH");
                break;
            case "BACK-INFO":
                nameVal = name.getText();
                xVal = xField.getText();
                yVal = yField.getText();
                layout.show(p, "START");
                break;
            case "BACK-CSV":
                layout.show(p, "CHOOSE");
                break;
            case "BACK-MANUAL":
                dataStore();
                if (manualPage == 0) {
                    layout.show(p, "CHOOSE");
                } else {
                    manualPage--;
                    layout.show(p, "MANUAL");
                    if (!visited[manualPage]) {
                        for (JTextField field : fields) {
                            field.setText("");
                        }
                    } else {
                        for (int i = 0; i <= 9; i++) {
                            if (i <= 4) {
                                fields[i].setText((String) manualStore[manualPage][i][0]);
                            } else {
                                fields[i].setText((String) manualStore[manualPage][i - 5][1]);
                            }
                        }
                    }
                }
                break;
            case "BACK-SELECT":
                layout.show(p, "INFO");
                name.setText(nameVal);
                xField.setText(xVal);
                yField.setText(yVal);
                break;
            case "PIE":
            case "BAR":
                mode = e.getActionCommand();
                layout.show(p, "INFO");
                name.setText(nameVal);
                xField.setText(xVal);
                yField.setText(yVal);
                break;
        }
    }

    public static void main(String[] args) {
        GraphGUI gui = new GraphGUI();
        gui.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        gui.setVisible(true);
    }
}
