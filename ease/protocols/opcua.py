#!/usr/bin/python
###############################################################################
#
# File Name         : opcua.py
# Created By        : Thomas Aurel
# Creation Date     : June 30th, 2016
# Version           : 0.1
# Last Change       : July  5th, 2016 at 04:59:47 PM
# Last Changed By   : Thomas Aurel
# Purpose           : Description
#
###############################################################################
import struct

from scapy.fields import (LEFieldLenField, LEIntField, LELongField,
                          LEShortField, PacketField, StrFixedLenField,
                          StrLenField, X3BytesField, XByteField)
from scapy.packet import Packet


class LenStringPacket(Packet):
    name = "len string packet"
    fields_desc = [
            LEFieldLenField('lenght', None, length_of='data', fmt="<I"),
            StrLenField('data', '', length_from=lambda pkt:pkt.lenght),
            ]


# Hello & Acknowledge {{{
# #############################################################################
#   OPCUA Hello message
# #############################################################################


class OPCUAHelloRequest(Packet):
    """
    """
    name = "OPCUA Hello Message Request"
    fields_desc = [
        StrFixedLenField('messageType', "HEL", 3),
        XByteField('chunckType', 0x46),
        LEIntField('messageSize', 0),
        LEIntField('version', 0),
        LEIntField('receiveBufferSize', 0xffff0000),
        LEIntField('sendBufferSize', 0xffff0000),
        LEIntField('maxMessageSize', 0x00004000),
        LEIntField('maxChunckCount', 0),
        # PacketField('endPointUrl', None, LenStringPacket)
        LEFieldLenField(
            'lenEndPointUrl', None, length_of='endPointUrl', fmt='<I'),
        StrLenField('endPointUrl', "", length_from=lambda x:x.lenEndPointUrl)
        ]


class OPCUAAckResponse(Packet):
    """

    """
    name = "OPCUA Acknowledge Message"
    fields_desc = [
            StrFixedLenField('messageType', "ACK", 3),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0x1c000000),
            LEIntField('version', 0x00000000),
            LEIntField('receiveBufferSize', 0xffff0000),
            LEIntField('sendBufferSize', 0xffff0000),
            LEIntField('maxMessageSize', 0x00004000),
            LEIntField('maxChunckCount', 0x00000000),
            ]
# }}}

# Open {{{
# #############################################################################
#   OPCUA Open Secure Channel
# #############################################################################


class OPCUAOpenSecureChannelIdRequest(Packet):
    name = "Open Secure Channel Id Request"
    fields_desc = [
            StrFixedLenField('messageType', "OPN", 3),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0),
            LEIntField('secureChannelId', 0),
            # PacketField('endPointUrl', None, LenStringPacket),
            LEFieldLenField(
                'lenSecurityPolicyUri', None, length_of='securityPolicyUri',
                fmt='<I'
                ),
            StrLenField(
                'securityPolicyUri', "",
                length_from=lambda pkt:pkt.lenSecurityPolicyUri,
                ),
            LEIntField('senderCertificate', 0xffffffff),
            LEIntField('receiverCertificate', 0xffffffff),
            LEIntField('sequenceNumber', 0),
            LEIntField('requestId', 0),
            # Message: Encodeable Object
            # ExpandNodeId
            XByteField('nodeIdEncodingMask', 1),
            XByteField('nodeIdNamespaceIndex', 0),
            LEShortField('nodeIdIdentifierNumeric', 446),
            # Open Secure Channel Request
            # Request Header
            LEShortField('authentificationToken', 0),
            LELongField('timestamp', 0),
            LEIntField('requestHandle', 0),
            LEIntField('returnDiagnostic', 0),
            LEIntField('auditEntryId', 0xffffffff),
            LEIntField('timeoutHint', 0),
            # Additional Header, Extension Object
            LEShortField('typeId', 0),
            XByteField('encodingMask', 0),
            LEIntField('clientProtocolVersion', 0),
            LEIntField('securityTokenRequestType', 0),
            LEIntField('messageSecurityMode', 1),
            LEIntField('clientNonce', 0),
            LEIntField('requestLifetime', 3600000)
            ]


class OPCUAOpenSecureChannelIdResponse(Packet):
    name = "Open Secure Channel Id Response"
    fields_desc = [
            StrFixedLenField('messageType', "OPN"),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0x87000000),
            LEIntField('secureChannelId', 0x00000000),
            # PacketField('securityPolicyUri', None, LenStringPacket),
            LEFieldLenField(
                'lenSecurityPolicyUri',
                None,
                length_of='securityPolicyUri',
                fmt="<I",
                ),
            StrLenField(
                'securityPolicyUri', "",
                length_from=lambda pkt:pkt.lenSecurityPolicyUri
                ),
            LEIntField('senderCertificate', 0xffffffff),
            LEIntField('receiverCertificate', 0xffffffff),
            LEIntField('sequenceNumber', 0x00000000),
            LEIntField('requestId', 0x00000000),
            # Message: Encodeable Object
            # ExpandNodeId
            XByteField('nodeIdEncodingMask', 0x01),
            XByteField('nodeIdNamespaceIndex', 0x00),
            LEShortField('nodeIdIdentifierNumeric', 0xc101),
            # Open Secure Channel Request
            # Response Header
            LELongField('timestamp', 0x0000000000000000),
            LEIntField('requestHandle', 0x00000000),
            LEIntField('serviceResult', 0x00000000),
            XByteField('serviceDiagnostics', 0x00),
            LEIntField('stringTable', 0x00000000),
            # Additional Header, Extension Object
            LEShortField('typeId', 0x0000),
            XByteField('encodingMask', 0x00),
            LEIntField('serverProtocolVersion', 0x00000000),
            # Security Token
            LEIntField('channelId', 0x00000000),
            LEIntField('tokenId', 0x00000000),
            LELongField('createat', 0x0000000000000000),
            LEIntField('revisedLifetime', 0x00000000),
            XByteField('serverNonce', 0x00)
            ]
# }}}

# #############################################################################
#   UA Secure Conversation Message
# #############################################################################


class OPCUACreateSessionRequest(Packet):
    """

    """
    name = "UA Secure Conversation Message Create Session Request"
    fields_desc = [
            StrFixedLenField('messageType', "MSG"),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0),
            LEIntField('secureChannelId', 0),
            LEIntField('securityToken', 0),
            LEIntField('securitySequenceNumber', 0),
            LEIntField('securityRequestId', 0),
            # OPCUA Service Encodeable Object
            XByteField('nodeIdEncodingMask', 1),
            XByteField('nodeIdNamespaceIndex', 0),
            LEShortField('nodeIdIdentifierNumeric', 461),
            # Create Session Request
            # Request Header
            LEShortField('authentificationToken', 0),
            LEIntField('requestHandle', 0),
            LEIntField('returnDiagnostic', 0),
            LEIntField('auditEntryId', 0xffffffff),
            LEIntField('timeoutHint', 0),
            # Additional Header, Extension Object
            LEShortField('typeId', 0),
            XByteField('encodingMask', 0),
            # Client Description Application Description
            # PacketField('applicationUri', None, LenStringPacket),
            LEFieldLenField(
                'lenApplicationUri', None, length_of='applicationUri', fmt="<I"
                ),
            StrLenField(
                'applicationUri', '',
                length_from=lambda pkt:pkt.lenApplicationUri
                ),
            # PacketField('productUri', None, LenStringPacket),
            LEFieldLenField(
                'lenProductUri', None, length_of='productUri', fmt='<I'
                ),
            StrLenField(
                'productUri', '', length_from=lambda pkt:pkt.lenProductUri
                ),
            # Application Name
            XByteField('encodingMask', 2),
            # PacketField('lenText', None, LenStringPacket),
            LEFieldLenField('lenText', None, length_of='text', fmt="<I"),
            StrLenField('text', 'UA Sample Client', ),
            LEIntField('applicationType', "0x00000000"),  # 1 pour 'Client'
            LEIntField('gatewayServerUri', 0xffffffff),
            LEIntField('discoveryProfileUri', 0xffffffff),
            LEIntField('discoveryUrls', 0x00000000),
            # PacketField('serverUri', None, LenStringPacket),
            LEFieldLenField(
                'lenServerUri', None, length_of='serverUri', fmt='<I'),
            StrLenField(
                    'serverUri', "", length_from=lambda pkt:pkt.lenServerUr),
            # PacketField('endPointUrl', None, LenStringPacket),
            LEFieldLenField(
                    'lenEndPointUrl', None, length_of='endPointUrl', fmt='<I'),
            StrLenField(
                    'endPointUrl', "",
                    length_from=lambda pkt:pkt.lenEndPointUrl),
            # PacketField('sessionName', None, LenStringPacket),
            LEFieldLenField(
                    'lenSessionName', None, length_of='sessionName', fmt='<I'),
            StrLenField(
                    'sessionName', "",
                    length_from=lambda pkt:pkt.lenSessionName
                    ),
            # PacketField('clientNonce', None, LenStringPacket),
            LEFieldLenField(
                    'lenClientNonce', None,
                    length_of='clientNonce', fmt='<I',
                    ),
            StrLenField(
                    'clientNonce', "",
                    length_from=lambda pkt:pkt.lenClientNonce
                    ),
            LEIntField('clientCertificate', 0xffffffff),
            LELongField('requestSessionTimeout', 0x00000000804f2241),
            LEIntField('maxResponseSize', 0x00004000)
            ]


class OPCUACreateSessionResponse(Packet):
    """

    """
    name = "UA Secure Conversation Message Create Session Response"
    fields_desc = [
            X3BytesField('messageType', "MSG"),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0xe02e0000),
            LEIntField('secureChannelId', 0x00000000),
            LEIntField('securityToken', 0x00000000),
            LEIntField('securitySequenceNumber', 0x00000000),
            LEIntField('securityRequestId', 0x00000000),
            # OPCUA Service Encodeable Object
            XByteField('nodeIdEncodingMask', 0x01),
            XByteField('nodeIdNamespaceIndex', 0x00),
            LEShortField('nodeIdIdentifierNumeric', 0xcd01),
            # Create Session Response
            # Response Header
            LELongField('timestamp', 0x0000000000000000),
            LEIntField('requestHandle', 0x00000000),
            LEIntField('serviceResult', 0x00000000),
            XByteField('serviceDiagnostics', 0x00),
            LEIntField('stringTable', 0x00000000),
            # Additional Header, Extension Object
            LEShortField('typeId', 0x0000),
            XByteField('encodingMask', 0x00),
            # Session Id
            XByteField('sessionIdNodeId', 0x02),
            LEShortField('sessionIdNamespaceIndex', 0x0600),
            LEIntField('sessionIdIdentifierNumeric', 0x00000000),
            # Authentification Token
            XByteField('authentificationTokenNodeId', 0x00),
            LEShortField('authentificationTokenIdNamespaceIndex', 0x0600),
            PacketField(
                'authentificationTokenIdentifierByteString',
                None,
                LenStringPacket
                ),
            # LEFieldLenField(
            #     'lenAuthentificationTokenIdentifierByteString', "",
            #     length_of='authentificationTokenIdentifierByteString',
            #     fmt='<I'
            #     ),
            # StrLenField(
            #     'authentificationTokenIdentifierByteString', "",
            #     length_from=lambda \
            #     pkt:pkt.lenAuthentificationTokenIdentifierByteString
            #     ),
            LELongField('revisedSessionTimeout', 0x0000000000000000),
            PacketField('serverNonce', None, LenStringPacket),
            # LEFieldLenField(
            #     'lenServerNonce', None, length_of='serverNonce', fmt='<I'),
            # StrLenField(
            #     'serverNonce', "",
            #     length_from=lambda pkt:pkt.lenServerNonce),
            ]


class OPCUAActiveSessionRequest(Packet):
    """

    """
    name = "UA Secure Conversation Message Active Session Request"
    fields_desc = [
            X3BytesField('messageType', "MSG"),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0xe02e0000),
            LEIntField('secureChannelId', 0x00000000),
            LEIntField('securityToken', 0x00000000),
            LEIntField('securitySequenceNumber', 0x00000000),
            LEIntField('securityRequestId', 0x00000000),
            # OPCUA Service Encodeable Object
            XByteField('nodeIdEncodingMask', 0x01),
            XByteField('nodeIdNamespaceIndex', 0x00),
            LEShortField('nodeIdIdentifierNumeric', 0x0000),
            # Active Session Request
            # Request Header Active Session Request
            XByteField('authentificationTokenNodeId', 0x00),
            LEShortField('authentificationTokenIdNamespaceIndex', 0x0000),
            PacketField(
                'authentificationTokenIdentifierByteString',
                None,
                LenStringPacket
                ),
            # LEFieldLenField(
            #     'lenAuthentificationTokenIdentifierByteString', None,
            #     length_of='authentificationTokenIdentifierByteString',
            #     fmt='<I'
            #     ),
            # StrLenField(
            #     'authentificationTokenIdentifierByteString', "",
            #     length_from=lambda \
            #     pkt:pkt.lenAuthentificationTokenIdentifierByteString
            #     ),
            LELongField('timestamp', 0x0000000000000000),
            LEIntField('requestHandle', 0x02000000),
            LEIntField('returnDiagnostic', 0xff030000),
            LEIntField('auditEntryId', 0xffffffff),
            LEIntField('timeoutHint', 0x000000),
            # Additional Header Extension Object
            LEShortField('typeId', 0x0000),
            XByteField('encodingMask', 0x00),
            # Client Signature
            LEIntField('algorithm', 0xffffffff),
            LEIntField('signature', 0xffffffff),
            # LEIntField('arraySize', 0x00000000),
            ]


class OPCUAActiveSessionResponse(Packet):
    """

    """
    name = "UA Secure Conversation Message Active Session Request"
    fields_desc = [
            X3BytesField('messageType', "MSG"),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0xe02e0000),
            LEIntField('secureChannelId', 0x00000000),
            LEIntField('securityToken', 0x00000000),
            LEIntField('securitySequenceNumber', 0x00000000),
            LEIntField('securityRequestId', 0x00000000),
            # OPCUA Service Encodeable Object
            XByteField('nodeIdEncodingMask', 0x01),
            XByteField('nodeIdNamespaceIndex', 0x00),
            LEShortField('nodeIdIdentifierNumeric', 0x0000),
            ]


opcuaconversationmessage = {
        400: OPCUACreateSessionRequest,
        400: OPCUACreateSessionResponse,
        400: OPCUAActiveSessionRequest,
        400: OPCUAActiveSessionResponse,
        }


class OPCUASecureConversationMessageRequest(Packet):
    name = "UA Secure Conversation Message Request"
    fields_desc = [
            X3BytesField('messageType', "MSG"),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0xe02e0000),
            LEIntField('secureChannelId', 0x00000000),
            LEIntField('securityToken', 0x00000000),
            LEIntField('securitySequenceNumber', 0x00000000),
            LEIntField('securityRequestId', 0x00000000),
            # OPCUA Service Encodeable Object
            XByteField('nodeIdEncodingMask', 0x01),
            XByteField('nodeIdNamespaceIndex', 0x00),
            LEShortField('nodeIdIdentifierNumeric', 0x0000),
            ]

    @classmethod
    def dispatch_hook(cls, _pkt, *args, **kwargs):
        if _pkt and(_pkt) >= 26:
            if struct.unpack('!H', _pkt[26:28])[0] in opcuaconversationmessage:
                return opcuaconversationmessage[
                        struct.unpack('!H', _pkt[26:28])[0]](_pkt)
        return cls


class OPCUASecureConversationMessageResponse(Packet):
    name = "UA Secure Conversation Message Response"
    fields_desc = [
            X3BytesField('messageType', "MSG"),
            XByteField('chunckType', 0x46),
            LEIntField('messageSize', 0x00000000),
            LEIntField('secureChannelId', 0x00000000),
            LEIntField('securityToken', 0x00000000),
            LEIntField('securitySequenceNumber', 0x00000000),
            LEIntField('securityRequestId', 0x00000000),
            # OPCUA Service Encodeable Object
            XByteField('nodeIdEncodingMask', 0x01),
            XByteField('nodeIdNamespaceIndex', 0x00),
            LEShortField('nodeIdIdentifierNumeric', 0x0000)
            ]

    @classmethod
    def dispatch_hook(cls, _pkt, *args, **kwargs):
        if _pkt and(_pkt) >= 26:
            if struct.unpack('!H', _pkt[26:28])[0] in opcuaconversationmessage:
                return opcuaconversationmessage[
                        struct.unpack('!H', _pkt[26:28])[0]](_pkt)
        return cls

# #############################################################################
#   OPCUA Response Decoder
# #############################################################################

response = {
        "ACK": OPCUAAckResponse,
        "OPN": OPCUAOpenSecureChannelIdResponse,
        "MSG": OPCUASecureConversationMessageResponse
        }


def opcuaResponseDecoder(payload):
    message_type = payload[0:3]
    return response[message_type](payload)
