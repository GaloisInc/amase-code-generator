/*
 * This software was developed by AFRL/RBCD, a U. S. Government Agency<br/>
 * For controlled distribution contact:<br/>
 *
 * Air Vehicles Technology Assessment and Simulation Branch (AFRL/RBCD)
 * 2180 8th Street<br/>
 * WPAFB, Ohio 45433<br/>
 * <br/>
 * THIS IS GOVERNMENT OWNED SOFTWARE. The User shall not use or permit use of this
 * software for profit or in any manner offer it for sale. Software shall not be
 * disclosed or transferred to any activity or firm without the prior written
 * approval from the government assigned agency, currently AFRL/RBCD.<br/>
 * <br/>
 * This software is distributed WITHOUT ANY WARRANTY; without even
 * the implied warranty of MERCHANTABILITY or FITNESS FOR A
 * PARTICULAR PURPOSE.  In no event shall the contributors or the
 * Government be liable for any loss or for any indirect, special,
 * punitive, exemplary, incidental, or consequential damages arising from the
 * use, possession or performance of this software.<br/>
 */

package afrl.cmasi;


import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import afrl.cmasi.SessionStatus;
import avtas.lmcp.*;

/**
         The base class for all task requests passed to the automation service.  Task requests are not assigned to a specific vehicle, but         allow the automation service to determine the best vehicle to complete the task.         
*/
public class Play extends avtas.lmcp.LMCPObject {
    
    public static final int LMCP_TYPE = 61;

    public static final String SERIES_NAME = "CMASI";
    /** Series Name turned into a long for quick comparisons. */
    public static final long SERIES_NAME_ID = 4849604199710720000L;
    public static final int SERIES_VERSION = 3;


    private static final String TYPE_NAME = "Play";

    /**  A unique identifier for this Play. (Units: None)*/
    @LmcpType("int64")
    protected long PlayID = 0L;
    /**  A unique identifier for this Play. (Units: None)*/
    @LmcpType("int64")
    protected long UAVID = 0L;
    /**  An optional text string for the task. This is not necessarily unique, and is included for information only. TaskID should be used to uniquely identify tasks. (Units: None)*/
    @LmcpType("string")
    protected String Label = "";
    /**  A list of entity IDs that are eligible to accomplish this task. If the list is empty, then it is assumed all entities are eligible. (Units: None)*/
    @LmcpType("int64")
    protected java.util.ArrayList<Long> EligibleEntities = new java.util.ArrayList<Long>();
    /**  If a task is to be repeatedly done, this field indicates how often. A value of zero means the task is complete on the first pass. (Units: sec)*/
    @LmcpType("real32")
    protected float RevisitRate = (float)0;
    /**  An optional text string for automation service task parameters. (Units: None)*/
    @LmcpType("KeyValuePair")
    protected java.util.ArrayList<afrl.cmasi.KeyValuePair> Parameters = new java.util.ArrayList<afrl.cmasi.KeyValuePair>();
    /**  The priority value for this task. Priority is a relative value of this task compared to other tasks in the scenario. This field should be limited to the range[0..100], 100 being the highest level of priority. The exact interpretation priority may vary depending on algorithm implementation. (Units: None)*/
    @LmcpType("byte")
    protected short Priority = (byte)0;
    /**  Indicates whether this task <i><b>must</b></i> be executed as part of a mission plan. (Units: None)*/
    @LmcpType("bool")
    protected boolean Required = true;
    @LmcpType("int64")
    protected long Time = 0L;
    @LmcpType("SessionStatus")
    protected SessionStatus Status = new SessionStatus();

    
    public Play() {
    }

    public Play(long PlayID, String Label, float RevisitRate, short Priority, boolean Required, long Time, long UAVID){
        this.PlayID = PlayID;
        this.Label = Label;
        this.RevisitRate = RevisitRate;
        this.Priority = Priority;
        this.Required = Required;
        this.Time = Time;
        this.UAVID = UAVID;
    }


    public Play clone() {
        try {
            java.io.ByteArrayOutputStream bos = new java.io.ByteArrayOutputStream( calcSize() );
            pack(bos);
            java.io.ByteArrayInputStream bis = new java.io.ByteArrayInputStream(bos.toByteArray());
            Play newObj = new Play();
            newObj.unpack(bis);
            return newObj;
        } catch (IOException ex) {
            ex.printStackTrace();
            return null;
        }
    }
     
    /**  A unique identifier for this task. (Units: None)*/
    public long getPlayID() { return PlayID; }
    public long getUAVID() { return UAVID; }
    /**  A unique identifier for this task. (Units: None)*/
    public Play setPlayID( long val ) {
        PlayID = val;
        return this;
    }
    
    public Play setUAVID(long b) {
        UAVID = b;
        return this;
    }
    
    /**  An optional text string for the task. This is not necessarily unique, and is included for information only. TaskID should be used to uniquely identify tasks. (Units: None)*/
    public String getLabel() { return Label; }

    /**  An optional text string for the task. This is not necessarily unique, and is included for information only. TaskID should be used to uniquely identify tasks. (Units: None)*/
    public Play setLabel( String val ) {
        Label = val;
        return this;
    }
    public Play setTime(long t) {
        Time = t;
        return this;
    }
    
    public long getTime() { return Time; }

    public java.util.ArrayList<Long> getEligibleEntities() {
        return EligibleEntities;
    }

    /**  If a task is to be repeatedly done, this field indicates how often. A value of zero means the task is complete on the first pass. (Units: sec)*/
    public float getRevisitRate() { return RevisitRate; }

    /**  If a task is to be repeatedly done, this field indicates how often. A value of zero means the task is complete on the first pass. (Units: sec)*/
    public Play setRevisitRate( float val ) {
        RevisitRate = val;
        return this;
    }

    public java.util.ArrayList<afrl.cmasi.KeyValuePair> getParameters() {
        return Parameters;
    }

    /**  The priority value for this task. Priority is a relative value of this task compared to other tasks in the scenario. This field should be limited to the range[0..100], 100 being the highest level of priority. The exact interpretation priority may vary depending on algorithm implementation. (Units: None)*/
    public short getPriority() { return Priority; }

    /**  The priority value for this task. Priority is a relative value of this task compared to other tasks in the scenario. This field should be limited to the range[0..100], 100 being the highest level of priority. The exact interpretation priority may vary depending on algorithm implementation. (Units: None)*/
    public Play setPriority( short val ) {
        Priority = val;
        return this;
    }

    /**  Indicates whether this task <i><b>must</b></i> be executed as part of a mission plan. (Units: None)*/
    public boolean getRequired() { return Required; }

    /**  Indicates whether this task <i><b>must</b></i> be executed as part of a mission plan. (Units: None)*/
    public Play setRequired( boolean val ) {
        Required = val;
        return this;
    }



    public int calcSize() {
        int size = super.calcSize();  
        size += 14; // accounts for primitive types
        size += LMCPUtil.sizeOfString(Label);
        
        size += 2 + 8 * EligibleEntities.size();
        size += 2;
        size += LMCPUtil.sizeOfList(Parameters);

        return size;
    }

    public void unpack(InputStream in) throws IOException {
        PlayID = LMCPUtil.getInt64(in);
        UAVID = LMCPUtil.getInt64(in);

        Label = LMCPUtil.getString(in);

        EligibleEntities.clear();
        int EligibleEntities_len = LMCPUtil.getUint16(in);
        for(int i=0; i<EligibleEntities_len; i++){
            EligibleEntities.add(LMCPUtil.getInt64(in));
        }
        RevisitRate = LMCPUtil.getReal32(in);

        Parameters.clear();
        int Parameters_len = LMCPUtil.getUint16(in);
        for(int i=0; i<Parameters_len; i++){
        Parameters.add( (afrl.cmasi.KeyValuePair) LMCPUtil.getObject(in));
        }
        Priority = LMCPUtil.getByte(in);

        Required = LMCPUtil.getBool(in);


    }

    public void pack(OutputStream out) throws IOException {
        LMCPUtil.putInt64(out, PlayID);
        LMCPUtil.putInt64(out, UAVID);
        LMCPUtil.putInt64(out, Time);
        LMCPUtil.putString(out, Label);
        LMCPUtil.putUint16(out, EligibleEntities.size());
        for(int i=0; i<EligibleEntities.size(); i++){
            LMCPUtil.putInt64(out, EligibleEntities.get(i));
        }
        LMCPUtil.putReal32(out, RevisitRate);
        LMCPUtil.putUint16(out, Parameters.size());
        for(int i=0; i<Parameters.size(); i++){
            LMCPUtil.putObject(out, Parameters.get(i));
        }
        LMCPUtil.putByte(out, Priority);
        LMCPUtil.putBool(out, Required);


    }

    public int getLMCPType() { return LMCP_TYPE; }

    public String getLMCPSeriesName() { return SERIES_NAME; }

    public long getLMCPSeriesNameAsLong() { return SERIES_NAME_ID; }

    public int getLMCPSeriesVersion() { return SERIES_VERSION; };

    public String getLMCPTypeName() { return TYPE_NAME; }

    public String toString() {
        return toXML("");
    }

    public String toXML(String ws) {
        StringBuffer buf = new StringBuffer();
        buf.append( ws + "<Play Series=\"CMASI\">\n");
        buf.append( ws + "  <PlayID>" + String.valueOf(PlayID) + "</PlayID>\n");
        buf.append( ws + "  <Label>" + String.valueOf(Label) + "</Label>\n");
        buf.append( ws + "  <EligibleEntities>\n");
        for (int i=0; i<EligibleEntities.size(); i++) {
        buf.append( ws + "  <int64>" + String.valueOf(EligibleEntities.get(i)) + "</int64>\n");
        }
        buf.append( ws + "  </EligibleEntities>\n");
        buf.append( ws + "  <RevisitRate>" + String.valueOf(RevisitRate) + "</RevisitRate>\n");
        buf.append( ws + "  <Parameters>\n");
        for (int i=0; i<Parameters.size(); i++) {
            buf.append( Parameters.get(i) == null ? ( ws + "    <null/>\n") : (Parameters.get(i).toXML(ws + "    ")) + "\n");
        }
        buf.append( ws + "  </Parameters>\n");
        buf.append( ws + "  <Priority>" + String.valueOf(Priority) + "</Priority>\n");
        buf.append( ws + "  <Required>" + String.valueOf(Required) + "</Required>\n");
        buf.append( ws + "</Play>");

        return buf.toString();
    }

    public boolean equals(Object anotherObj) {
        if ( anotherObj == this ) return true;
        if ( anotherObj == null ) return false;
        if ( !(anotherObj instanceof Play) ) return false;
        if ( !super.equals(anotherObj) ) return false;
        Play o = (Play) anotherObj;
        if (PlayID != o.PlayID) return false;
        if (Label == null && o.Label != null) return false;
        if ( Label!= null && !Label.equals(o.Label)) return false;
        if (!EligibleEntities.equals( o.EligibleEntities)) return false;
        if (RevisitRate != o.RevisitRate) return false;
        if (!Parameters.equals( o.Parameters)) return false;
        if (Priority != o.Priority) return false;
        if (Required != o.Required) return false;

        return true;
    }

    public int hashCode() {
        int hash = 0;
        hash += 31 * (int)RevisitRate;

        return hash + super.hashCode();
    }

    
}

/* Distribution A. Approved for public release. 
 *  Case: #88ABW-2015-4601. Date: 24 Sep 2015. */