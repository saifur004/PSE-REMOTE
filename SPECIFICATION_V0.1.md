# Specification for autonomous model car driving (V 0.1)

## Purpose of this specification

The purpose of this specification is to provide an extensive, fast and expandable interface
so that any autonomous car can be controlled in a basic way.
Special features (for cars or controllers) can be defined in the scope of this specification to be used in a single group
but must not be supported by every group. 

## Connections / Protocols

The car needs to implement the following minimal connections:
- gRPC Server for command sending on port 2069
- UDP Server for control/feedback on port 2070
- WebRTC Server for video streaming on a dynamic port

## gRPC for command sending

The gRPC connection is for sending reliable commands to the car.
They are used to set up video connections or get one time information such as battery charge or general device information.

### The commands

The commands are defined in a provided "*commands.proto*" file.
This guaranties the same serialization over different languages and devices.
This file includes the following rpc commands:
```protobuf
service CommandsService {
    rpc Heartbeat (Void) returns (Void);

    rpc GetCameraProtocols (Void) returns (SupportedStreamsReply);
    rpc StartCamera (CamStreamStartRequest) returns (CamStreamPort);
    rpc StopCamera (CamStreamPort) returns (Void);

    rpc ResetUdp(Void) returns (Void);

    rpc GetGpsCoordinates (Void) returns (GpsCoordinates);
    rpc GetProcessorStatus (Void) returns (ProcessorData);
    rpc GetBatteryStatus (Void) returns (BatterData);
    rpc GetGeneralInformation (Void) returns (GeneralInformationData);
}
```

### Video protocols

For cross group compatibility each car should support **WebRTC** for streaming.
To further provide the option for different streaming protocols you can define the protocol when requesting the stream.
This gives the possibility to test other protocols which are for example needed by special hardware (like a VR headset)


## Custom UDP for car control/feedback

The UDP connection is for sending ordered by unreliable real time control signals to the car or get sensor feedback.
As UDP does not provide support for ordered packets we need to implement this feature on our own.

### Custom UDP protocol

One UDP packet contains the packet order number, payload type followed by the actual payload.
The order number is an unsigned 16-bit number (ushort), ongoing and overflowing **per payload type**.
The payload type is an unsigned byte identifying the payload.

      0               7 8              15 
     +--------+--------+--------+--------+ 
     |            Order Number           | 
     |                                   | 
     +--------+--------+--------+--------+ 
     |     Payload     |     Payload     . 
     |      Type       |                 .
     +--------+--------+--------... 

#### Order Number

The ongoing increasing and overflowing characteristics need to be implemented by each group on each car/controller.
On boot the sender sets the order number for the used payload type to a random starting number.
Before the first communication the controller send a *ResetUdp()* command via gRPC (and also resets the own udp state).
With each packet send the static order number for the payload used is increased by one.
When the receiver receives a packet they store the order number linked to the payload type.
If the received packet has an order number lower than the stored "last-received-order-number" the packet is ignored.
If the stored number is above 65503 (65535 - 32) and the received number below 32 the packet should be handled like a continuing order.
When a long package lost occurs the receiver will maybe not catch the order number overflow. In this case the controller needs to issue a *ResetUdp()* command via gRPC.

#### Payload Type

| Value | Payload Type       |
|-------|--------------------|
| 0     | Reserved / Unknown |
| 1     | Car Control        |

Every group needs to implement "Car Control", defined in "*controls.proto*".
Payload types not supported by the car or controller can be completely ignored.
Custom real time communication can be added with an individual/custom serialization or with a custom proto file including "*controls.proto*".

## Basic WebRTC

*to be defined and investigated*

## Extensibility with a future prove specification

As the project is a rapid prototyping environment and subject to spontaneous changes in requirements and challenges
this specification provides the bare minimum for intergroup workability.
It also gives room to implement custom interface extensions for special features for the used hardware.
For an error free compatibility following guidelines should be followed:
- Custom UDP payload types (number) should be known by all groups and noted in a centralized documentation. That way car/controller should not send a data format which is not expected by the receiver bc of a shared usage of a concrete payload type number.
- If multiple groups have the same needs a standardised payload type can be included in this document / proto files.
- Same rules apply to video protocols inside of *commands.proto*
- Same rules apply to the tcp commands inside of *commands.proto*

Protobuf has a guideline for updating proto files in a compatible way [here](https://protobuf.dev/programming-guides/proto3/#assigning).

## Further specification

To have an easy way of connection to and from Darmstadt/Kokkola the use of a direct client to client tunnel is advised.
This tunnel should have the same software and configuration (also password) on all cars.
Which protocol/software is best for our purpose is yet to be investigated.
