
//dimensions measured with calipers and confirmed here:
//https://www.electronics-lab.com/raspberry-pi-zero-footprint-and-dimensions/
//This does not have the camera port

pi_z_1_3_w = 30;
pi_z_1_3_l = 65;
pi_z_1_3_spacing_w = 23;
pi_z_1_3_spacing_l = 58;

outter_spacing = 3;
pi_z_1_3_outter_spacing_w = pi_z_1_3_spacing_w + outter_spacing;
pi_z_1_3_outter_spacing_l = pi_z_1_3_spacing_l + outter_spacing;
pi_z_1_3_inner_spacing_w = pi_z_1_3_spacing_w - outter_spacing;
pi_z_1_3_inner_spacing_l = pi_z_1_3_spacing_l - outter_spacing;

pi_z_1_3_hole_d = 2.65;
pi_z_1_3_spacer_d = 4;
pi_z_1_3_hole_padding = 3.5;
pi_z_1_3_corner_d = 9.25;

micro_usb_w = 8.45;
micro_usb_h = 4.25;

mini_hdmi_w = 12;
mini_hdmi_h = 5.25;

micro_sdcard_w = 13;
micro_sdcard_h = 6;

pi_z_1_3_camera_w = 18.5;
pi_z_1_3_camera_h = 3;

pi_z_1_3_h = 1.5;

pi_z_1_3_hdmi_middle = 12.4;
pi_z_1_3_usb1_middle = 41.4;
pi_z_1_3_usb2_middle = 54;
pi_z_1_3_sdcard_middle = 16.9;

fn = 128;

thickness = 2;
lid_thickness = 2.75;
outter_height = 12;
padding = 0.75;

led_diam = 10.3; //9.8;
led_d = 19; //9.5;
led_w = 18; //22;
led_l = 53;
edge_space = 3;
led_space = 3.5;

module make_base()
{
    difference()
    {
        translate([-outter_spacing/2, -outter_spacing/2, 0])
        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = outter_height, $fn = fn);
            translate([pi_z_1_3_outter_spacing_l, 0, 0])cylinder(d = pi_z_1_3_corner_d, h = outter_height, $fn = fn);
            translate([pi_z_1_3_outter_spacing_l, pi_z_1_3_outter_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = outter_height, $fn = fn);
            translate([0, pi_z_1_3_outter_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = outter_height, $fn = fn);
        }

        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = outter_height+1, $fn = fn);
            translate([pi_z_1_3_spacing_l, 0, 0])cylinder(d = pi_z_1_3_corner_d, h = outter_height+1, $fn = fn);
            translate([pi_z_1_3_spacing_l, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = outter_height+1, $fn = fn);
            translate([0, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = outter_height+1, $fn = fn);
        }

        //camera
        //color("red")translate([-thickness*3,pi_z_1_3_spacing_w/2 - pi_z_1_3_camera_w/2-padding,thickness*2+pi_z_1_3_h])cube([thickness * 3,  pi_z_1_3_camera_w, pi_z_1_3_camera_h - pi_z_1_3_h]);

        //micro sdcard
        color("red")translate([-thickness*3 + pi_z_1_3_l,-micro_sdcard_w/2 + pi_z_1_3_sdcard_middle/2 + padding,thickness*2+pi_z_1_3_h])cube([thickness * 3,  micro_sdcard_w, micro_sdcard_h - pi_z_1_3_h]);


        //mini hdmi
        color("red")translate([-mini_hdmi_w/2+pi_z_1_3_l-pi_z_1_3_hole_d-pi_z_1_3_hdmi_middle - padding,pi_z_1_3_w-mini_hdmi_w/2,thickness*2+pi_z_1_3_h])cube([mini_hdmi_w, thickness * 3,  mini_hdmi_h - pi_z_1_3_h]);

        //micro usb1
        color("red")translate([-micro_usb_w/2+pi_z_1_3_l-pi_z_1_3_hole_d-pi_z_1_3_usb1_middle - padding,pi_z_1_3_w-micro_usb_w/2,thickness*2+pi_z_1_3_h])cube([micro_usb_w, thickness * 3,  micro_usb_h - pi_z_1_3_h]);

        //micro usb2
        color("red")translate([-micro_usb_w/2+pi_z_1_3_l-pi_z_1_3_hole_d-pi_z_1_3_usb2_middle - padding,pi_z_1_3_w-micro_usb_w/2,thickness*2+pi_z_1_3_h])cube([micro_usb_w, thickness * 3,  micro_usb_h - pi_z_1_3_h]);

    }


    //the mounting base
    color("green")
    {

        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([pi_z_1_3_spacing_l, 0, 0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([pi_z_1_3_spacing_l, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([0, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
        }

        cylinder(d = pi_z_1_3_hole_d, h = thickness * 3, $fn = fn);
        translate([pi_z_1_3_spacing_l, 0, 0])cylinder(d = pi_z_1_3_hole_d, h = thickness * 3, $fn = fn);
        translate([pi_z_1_3_spacing_l, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_hole_d, h = thickness * 3, $fn = fn);
        translate([0, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_hole_d, h = thickness * 3, $fn = fn);


        cylinder(d = pi_z_1_3_spacer_d, h = thickness * 2, $fn = fn);
        translate([pi_z_1_3_spacing_l, 0, 0])cylinder(d = pi_z_1_3_spacer_d, h = thickness * 2, $fn = fn);
        translate([pi_z_1_3_spacing_l, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_spacer_d, h = thickness * 2, $fn = fn);
        translate([0, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_spacer_d, h = thickness * 2, $fn = fn);
    }
}

module make_lid()
{
    //the mounting base
    color("green")
    {
       
        translate([-outter_spacing/2, -outter_spacing/2, 0])
        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([pi_z_1_3_outter_spacing_l, 0, 0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([pi_z_1_3_outter_spacing_l, pi_z_1_3_outter_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([0, pi_z_1_3_outter_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
        }
       translate([0,0,thickness])
       difference()
        {
        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = lid_thickness, $fn = fn);
            translate([pi_z_1_3_spacing_l, 0, 0])cylinder(d = pi_z_1_3_corner_d, h = lid_thickness, $fn = fn);
            translate([pi_z_1_3_spacing_l, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = lid_thickness, $fn = fn);
            translate([0, pi_z_1_3_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = lid_thickness, $fn = fn);
        }
        
        translate([+outter_spacing/2, +outter_spacing/2, 0])
        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = lid_thickness+1, $fn = fn);
            translate([pi_z_1_3_inner_spacing_l, 0, 0])cylinder(d = pi_z_1_3_corner_d, h = lid_thickness+1, $fn = fn);
            translate([pi_z_1_3_inner_spacing_l, pi_z_1_3_inner_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = lid_thickness+1, $fn = fn);
            translate([0, pi_z_1_3_inner_spacing_w, 0])cylinder(d = pi_z_1_3_corner_d, h = lid_thickness+1, $fn = fn);
        }
        }

    }
}

module make_led_holder()
{

   
    
    difference()
    {
        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([-pi_z_1_3_corner_d/2+pi_z_1_3_spacing_l, -pi_z_1_3_corner_d/2,0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness]);
            translate([0, led_w,0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([pi_z_1_3_spacing_l-pi_z_1_3_corner_d/2, led_w-pi_z_1_3_corner_d/2, 0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness]);
        }
        
        //slightly taller than the base, so the holes are clear in preview mode
        for( j = [0 : 2] )
            translate([1 + led_diam/2 + led_diam * j + led_space * j, led_w/2, -0.5])cylinder(d=led_diam, h=thickness+1, $fn=fn);
    }
    
    for ( i = [1 : 10] )
    {
        translate([0,0,thickness*i])
        difference()
        {
            hull()
            {
                cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
                translate([-pi_z_1_3_corner_d/2+pi_z_1_3_spacing_l, -pi_z_1_3_corner_d/2,0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness]);
                translate([0, led_w,0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
                translate([pi_z_1_3_spacing_l-pi_z_1_3_corner_d/2, led_w-pi_z_1_3_corner_d/2, 0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness]);
            }
            
            hull()
            {
                translate([edge_space, edge_space, -0.5])cylinder(d = pi_z_1_3_corner_d, h = thickness+1, $fn = fn);
                translate([-pi_z_1_3_corner_d/2+pi_z_1_3_spacing_l+1, -pi_z_1_3_corner_d/2+edge_space,-0.5])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness+1]);
                translate([edge_space, led_w-edge_space,-0.5])cylinder(d = pi_z_1_3_corner_d, h = thickness+1, $fn = fn);
                translate([pi_z_1_3_spacing_l-pi_z_1_3_corner_d/2+1, led_w-pi_z_1_3_corner_d/2-edge_space, -0.5])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness+1]);
            }
        }
    }
    
   
}

module make_led_holder_lid()
{
        color("yellow")
    {
        hull()
        {
            cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([-pi_z_1_3_corner_d/2+pi_z_1_3_spacing_l-1, -pi_z_1_3_corner_d/2,0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness]);
            translate([0, led_w,0])cylinder(d = pi_z_1_3_corner_d, h = thickness, $fn = fn);
            translate([pi_z_1_3_spacing_l-pi_z_1_3_corner_d/2-1, led_w-pi_z_1_3_corner_d/2-0.5, 0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness]);
        }
        
        translate([0,0,thickness])
        difference()
        { 
            hull()
            {
                translate([edge_space, edge_space, 0])cylinder(d = pi_z_1_3_corner_d, h = thickness*1.75+thickness*6, $fn = fn);
                translate([-pi_z_1_3_corner_d/2+pi_z_1_3_spacing_l-2.5, -pi_z_1_3_corner_d/2+edge_space,0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness*1.75+thickness*6]);
                translate([edge_space, led_w-edge_space,0])cylinder(d = pi_z_1_3_corner_d, h = thickness*1.75+thickness*6, $fn = fn);
                translate([pi_z_1_3_spacing_l-pi_z_1_3_corner_d/2-2.5, led_w-pi_z_1_3_corner_d/2-edge_space, 0])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness*1.75+thickness*6]);
            }
            hull()
            {
                translate([edge_space*2, edge_space*2, -0.5])cylinder(d = pi_z_1_3_corner_d, h = thickness*2+1+thickness*6, $fn = fn);
                translate([-pi_z_1_3_corner_d/2+pi_z_1_3_spacing_l+1, -pi_z_1_3_corner_d/2+edge_space*2,-0.5])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness*2+1+thickness*6]);
                translate([edge_space*2, led_w-edge_space*2,-0.5])cylinder(d = pi_z_1_3_corner_d, h = thickness*2+1+thickness*6, $fn = fn);
                translate([pi_z_1_3_spacing_l-pi_z_1_3_corner_d/2+1, led_w-pi_z_1_3_corner_d/2-edge_space*2, -0.5])cube([pi_z_1_3_corner_d, pi_z_1_3_corner_d, thickness*2+1+thickness*6]);
            }
            
            translate([46.25-2.3-edge_space*1.25,-(edge_space*2+1)/2,thickness*6])cube([edge_space*1.75,edge_space*2+1,edge_space*2+1]);
        }
    }

}

make_base();

translate([0,pi_z_1_3_w+pi_z_1_3_corner_d,pi_z_1_3_w+pi_z_1_3_corner_d/2])
rotate([-90,0,0])
translate([0,0,thickness*2+1])
{
    difference()
    {
    //bkd this isn't right - but it works (for now)
    translate([pi_z_1_3_corner_d/2+outter_spacing/21+0.75, pi_z_1_3_w-1, 0])
    rotate([180,0,0])make_lid();
        
    translate([pi_z_1_3_l/2-led_w/2+edge_space-4,pi_z_1_3_w-2.5*thickness-12,-thickness-0.1])    
    cube([pi_z_1_3_camera_w+2,20, 4]);
        
}


//pi_z_1_3_corner_d/2+pi_z_1_3_l/2+led_w-led_diam
translate([pi_z_1_3_corner_d/2+led_w/2+led_diam,pi_z_1_3_w+pi_z_1_3_corner_d/2+0.5,pi_z_1_3_corner_d/2+pi_z_1_3_spacing_l])
rotate([0,90,270])
make_led_holder();


}


translate([pi_z_1_3_spacing_l * 1.5, 0, 0])
make_led_holder_lid();
