/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javaapplication4;
import java.net.*;
import java.io.*;

/**
 *
 * @author Behrouz
 */
public class UDPClient {
   static class Test1 implements Test{
        private int t;
        public Test1(int i)
        {
            t=i;
        }
        public void print(){
            System.out.println("Test1 Value: "+t);
        }
   };
    public static void main(String[] args) {
        try{
         //DatagramSocket s=new DatagramSocket();
         MulticastSocket s=new MulticastSocket();
         s.joinGroup(InetAddress.getByName("225.1.1.1"));
         System.out.println(s.getLocalPort());
         Test1  t= new Test1(100000);
         //String t=new String("asdfsfdfdsd");
         ByteArrayOutputStream bos=new ByteArrayOutputStream();
         ObjectOutputStream os=new ObjectOutputStream(bos);
         os.writeObject(t);
         //first sending its size          
          byte[] size = new byte[4];
          for (int i = 0; i < 4; ++i) {
             int shift = i << 3; 
             size[3-i] = (byte)((bos.toByteArray().length & (0xff << shift)) >>> shift);
          }
          //DatagramPacket p=new DatagramPacket(size, 4, InetAddress.getByName("127.0.0.1"), 2000);
          DatagramPacket p=new DatagramPacket(size, 4, InetAddress.getByName("225.1.1.1"), 2000);
          s.send(p);
          ///NOW sending obj
          //DatagramPacket p2=new DatagramPacket(bos.toByteArray(), bos.toByteArray().length,  InetAddress.getByName("127.0.0.1"), 2000);
          DatagramPacket p2=new DatagramPacket(bos.toByteArray(), bos.toByteArray().length,  InetAddress.getByName("225.1.1.1"), 2000);
          s.send(p2);          
          System.out.println("sent: "+bos.toByteArray().length + " bytes");
        }catch(Exception e){
            e.printStackTrace();
        }
        //while (true);

    }

}
